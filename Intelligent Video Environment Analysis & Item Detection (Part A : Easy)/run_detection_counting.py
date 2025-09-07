#!/usr/bin/env python3
"""
simple_counting_analysis.py

Beginner-friendly wrapper for environment classification + item counting.
 - YOLOv8 detection (default yolov8n.pt)
 - Tracks & counts objects
 - Environment classification (home/shop heuristic)
 - Saves report.csv
 - Returns Python dict summary

Usage from another script / notebook:
    from simple_counting_analysis import analyze_video
    result = analyze_video("input.mp4", model_path="yolov8s.pt", save_video=True)
    print(result)
"""

import os, csv
from collections import defaultdict
from ultralytics import YOLO
import cv2

# IoU for tracking
def iou(boxA, boxB):
    xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
    xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
    inter = max(0, xB-xA) * max(0, yB-yA)
    areaA = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])
    union = areaA + areaB - inter
    return inter/union if union>0 else 0.0

# Environment heuristic
ENV_MAP = {
    'sofa':'home','bed':'home','tv':'home','refrigerator':'home','fridge':'home',
    'chair':'home','table':'home','microwave':'home','washing_machine':'home',
    'shelf':'shop','bottle':'shop','box':'shop','clothing':'shop','counter':'shop','display':'shop'
}

def analyze_video(video_path, model_path="yolov8n.pt", conf_thres=0.35,
                  imgsz=640, frame_skip=2, iou_thres=0.45, stale_frames=30,
                  save_video=False, output_path="output.mp4", out_csv="report.csv"):
    """
    Analyze a video and return results.
    Saves a report.csv with Environment, Item, Count.
    Returns a dict summary.
    """
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width, height = int(cap.get(3)), int(cap.get(4))

    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps/max(1,frame_skip), (width,height))
    else:
        out = None

    active_tracks, all_tracks, next_id, frame_idx = [], [], 1, 0
    env_votes = defaultdict(int)

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame_idx += 1
        if frame_idx % frame_skip: continue

        results = model(frame, imgsz=imgsz, conf=conf_thres)[0]
        detections=[]
        if hasattr(results,'boxes') and len(results.boxes):
            xyxy=results.boxes.xyxy.cpu().numpy()
            confs=results.boxes.conf.cpu().numpy()
            clss=results.boxes.cls.cpu().numpy().astype(int)
            names=results.names if hasattr(results,'names') else model.names
            for box,conf,cls in zip(xyxy,confs,clss):
                detections.append({'bbox':[float(box[0]),float(box[1]),float(box[2]),float(box[3])],
                                   'conf':float(conf),
                                   'class':str(names[int(cls)])})

        # Tracking + env votes
        for det in detections:
            bbox, cname = det['bbox'], det['class']
            if cname in ENV_MAP:
                env_votes[ENV_MAP[cname]] += 1
            best,best_iou=None,0.0
            for tr in active_tracks:
                if tr['class']!=cname: continue
                cur=iou(tr['bbox'],bbox)
                if cur>best_iou: best_iou, best=cur,tr
            if best and best_iou>=iou_thres:
                best['bbox']=bbox; best['last_seen']=frame_idx
            else:
                tr={'id':next_id,'class':cname,'bbox':bbox,
                    'first_seen':frame_idx,'last_seen':frame_idx}
                active_tracks.append(tr); all_tracks.append(dict(tr)); next_id+=1
        active_tracks=[t for t in active_tracks if frame_idx-t['last_seen']<=stale_frames]

        if save_video:
            for tr in active_tracks:
                x1,y1,x2,y2=map(int,tr['bbox'])
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame,f"{tr['class']} id:{tr['id']}",(x1,max(10,y1-5)),
                            cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,0),1)
            out.write(frame)

    cap.release()
    if save_video: out.release()

    # Counts
    counts=defaultdict(int)
    for t in all_tracks:
        counts[t['class']] += 1
    env_label=max(env_votes.items(),key=lambda x:x[1])[0] if env_votes else "unknown"

    # Save CSV
    with open(out_csv,'w',newline='') as f:
        w=csv.writer(f)
        w.writerow(["Environment","Item","Count"])
        for cname,cnt in counts.items():
            w.writerow([env_label,cname,cnt])

    # Summary dict
    summary={"environment":env_label,"counts":dict(counts),"csv":out_csv}
    return {"csv_file": out_csv}

# Demo
if __name__=="__main__":
    result=analyze_video("input.mp4", save_video=True)
    print("Result summary:", result)
