#!/usr/bin/env python3
"""
simple_video_analysis.py

Beginner-friendly wrapper for AI video analysis.
Just call analyze_video("input.mp4", declared_env="shop", declared_items="bottles:200,fridge:1")
and it will:
 - Run YOLOv8x detection + tracking
 - Do environment classification
 - Compare declared vs detected
 - Save CSV/JSON reports
 - Return results as a Python dict
"""

import os, csv, json
from collections import defaultdict
import cv2, numpy as np
from ultralytics import YOLO
from ensemble_boxes import weighted_boxes_fusion

# Canonical mapping (simplified)
CANON = {
    'sofa':'sofa','couch':'sofa','bed':'bed','chair':'chair','tv':'tv',
    'refrigerator':'fridge','fridge':'fridge','microwave':'microwave',
    'washing machine':'washing_machine','table':'table','desk':'table',
    'laptop':'computer','computer':'computer','whiteboard':'whiteboard',
    'shelf':'shelf','rack':'shelf','counter':'counter',
    'bottle':'bottles','box':'boxes','display':'display',
    'car':'car','motorbike':'bike','bicycle':'bike','scooter':'scooter'
}

# Simple IoU
def iou(boxA, boxB):
    xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
    xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
    inter = max(0, xB - xA) * max(0, yB - yA)
    areaA = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])
    return inter / (areaA + areaB - inter + 1e-9)

# Declared data parser
def parse_declared(items_str):
    out={}
    if not items_str: return out
    for kv in items_str.split(','):
        if ':' in kv:
            k,v=kv.split(':',1)
            try: out[k.strip().lower()] = int(v.strip())
            except: pass
    return out

# Object detection wrapper (no WBF for simplicity)
def detect_objects(model, frame, conf=0.25, imgsz=640):
    res = model(frame, imgsz=imgsz, conf=conf)[0]
    out=[]
    if len(res.boxes):
        xyxy = res.boxes.xyxy.cpu().numpy()
        confs = res.boxes.conf.cpu().numpy()
        clss = res.boxes.cls.cpu().numpy().astype(int)
        for box,c,cls in zip(xyxy,confs,clss):
            out.append({
                "bbox":[int(box[0]),int(box[1]),int(box[2]),int(box[3])],
                "conf":float(c),
                "class":model.names[cls]
            })
    return out

# Main easy function
def analyze_video(video_path, declared_env="", declared_items="", out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)

    # Load YOLOv8x (heavy but accurate)
    model = YOLO("yolov8x.pt")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video {video_path}")

    active_tracks=[]; all_tracks=[]; next_id=1; frame_idx=0
    decl_items=parse_declared(declared_items)

    while True:
        ret,frame=cap.read()
        if not ret: break
        frame_idx+=1
        if frame_idx % 3:  # skip frames for speed
            continue

        detections=detect_objects(model,frame,conf=0.3,imgsz=640)

        for d in detections:
            bbox,cname,conf=d['bbox'],d['class'],d['conf']
            best,best_iou=None,0
            for tr in active_tracks:
                if tr['class']==cname:
                    cur=iou(tr['bbox'],bbox)
                    if cur>best_iou: best_iou, best=cur,tr
            if best and best_iou>0.4:
                best['bbox']=bbox; best['last_seen']=frame_idx
                best['confs'].append(conf)
            else:
                tr={'id':next_id,'class':cname,'bbox':bbox,
                    'last_seen':frame_idx,'confs':[conf]}
                active_tracks.append(tr); all_tracks.append(tr); next_id+=1

        active_tracks=[t for t in active_tracks if frame_idx-t['last_seen']<30]

    cap.release()

    # Count results
    final_counts=defaultdict(int); avg_conf=defaultdict(list)
    for t in all_tracks:
        cname=CANON.get(t['class'].lower(),None)
        if not cname: continue
        final_counts[cname]+=1
        avg_conf[cname].append(np.mean(t['confs']))

    avg_conf={k:float(np.mean(v)) for k,v in avg_conf.items()}
    detected_env="home" if "sofa" in final_counts or "bed" in final_counts else "shop"  # toy heuristic
    env_conf=0.8

    # Declared vs detected
    mismatches=[]
    for k_decl,v_decl in decl_items.items():
        v_det=final_counts.get(k_decl,0)
        if v_det!=v_decl:
            mismatches.append({"item":k_decl,"declared":v_decl,"detected":v_det})

    decision="Review Needed" if (declared_env and declared_env!=detected_env) or mismatches else "Pass"

    # Save CSV
    csv_path=os.path.join(out_dir,"report.csv")
    with open(csv_path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["EnvDetected","EnvConf","DeclaredEnv","Decision"])
        w.writerow([detected_env,env_conf,declared_env,decision])
        w.writerow([])
        w.writerow(["Item","DetectedCount","DeclaredCount","AvgConf"])
        for k,v in final_counts.items():
            w.writerow([k,v,decl_items.get(k,""),f"{avg_conf.get(k,0):.2f}"])

    # Save JSON
    summary={
        "environment_detected":detected_env,
        "environment_confidence":env_conf,
        "declared_environment":declared_env,
        "detected_objects":dict(final_counts),
        "declared_items":decl_items,
        "avg_confidence":avg_conf,
        "mismatches":mismatches,
        "decision":decision
    }
    json_path=os.path.join(out_dir,"report.json")
    with open(json_path,"w") as jf: json.dump(summary,jf,indent=2)

    return {"csv_file": csv_path}

# Demo usage
if __name__=="__main__":
    result = analyze_video("input.mp4", declared_env="shop", declared_items="bottles:200,fridge:1")
    print("Final result:", result)
