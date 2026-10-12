# -*- coding: utf-8 -*-
"""
化学实验数据处理系统 · 网页版【版本 B：模拟器风】
=====================================================
参考 NovaSolver 的模拟器页面版式：
  深蓝顶栏（面包屑）+ 深蓝渐变 Hero + 浅灰页面
  左：参数设置（滑块 + 数值框，即时刷新）
  右：KPI 指标卡 + 标签页（结果明细 / 图表）
计算部分与版本 A 共用同一份定义（从 build.py 导入），保证数值一致。

运行：python build_v2.py
"""

import os
import sys

from build import EXPS, RUNTIME_MATH, WARN_JS, js_str, js_fields

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build", "B")


def log(text):
    sys.stdout.write(text + "\n")


# ============================================================
# 每页的分类标签（仅版本 B 用）
# ============================================================
PILL = {
    "exp1-mg-molar-mass": "物理化学 · 气体定律",
    "exp2-acetic-ka": "物理化学 · 电离平衡",
    "exp3-baso4-ksp": "物理化学 · 沉淀溶解平衡",
    "exp4-kinetics-ea": "化学动力学 · 速率与活化能",
    "exp5-complex-k": "配位化学 · 组成与稳定常数",
}

# ============================================================
# 滑块范围：min / max / step（键为 实验文件|字段key）
# ============================================================
RANGES = {
    "exp1-mg-molar-mass": {
        "m":  [5, 50, 0.1], "v1": [0, 20, 0.1], "v2": [0, 60, 0.1],
        "p":  [95000, 103000, 1], "t": [273.15, 308.15, 0.05],
    },
    "exp2-acetic-ka": {
        "c0": [0.02, 0.2, 0.005],
        "ph1": [2, 6, 0.01], "ph2": [2, 6, 0.01], "ph3": [2, 6, 0.01], "ph4": [2, 6, 0.01],
    },
    "exp3-baso4-ksp": {
        "cw": [0, 5e-6, 1e-8], "cs": [0, 1.2e-5, 1e-8], "t": [288.15, 303.15, 0.05],
    },
    "exp4-kinetics-ea": {
        "t1": [30, 900, 5], "t2": [30, 900, 5], "t3": [30, 900, 5],
        "t4": [30, 900, 5], "t5": [30, 900, 5],
        "T1": [285, 315, 0.05], "T2": [285, 315, 0.05], "T3": [285, 315, 0.05],
        "tt1": [20, 900, 5], "tt2": [20, 900, 5], "tt3": [20, 900, 5],
    },
    "exp5-complex-k": dict([("a%d" % i, [0, 1, 0.01]) for i in range(1, 12)]),
}


# ============================================================
# 样式
# ============================================================
CSS = r"""
  :root{
    --navy:#0f2557; --navy2:#132a63; --blue:#1d4ed8; --cyan:#0891b2;
    --ink:#0f172a; --dim:#64748b; --faint:#94a3b8;
    --bg:#f1f5f9; --card:#ffffff; --line:#e2e8f0;
    --ok:#16a34a; --warn:#d97706; --err:#dc2626;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{min-height:100%}
  body{
    font-family:"Microsoft YaHei UI","Microsoft YaHei","PingFang SC","Hiragino Sans GB",
                system-ui,-apple-system,"Segoe UI",sans-serif;
    background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased;
  }
  /* ---------- 顶栏 ---------- */
  .topbar{background:var(--navy);color:#9fb4d8;font-size:12px;
          padding:10px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}
  .crumb{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
  .crumb i{font-style:normal;color:#5c74a0}
  .crumb b{color:#fff;font-weight:700}
  .exp-select{
    font:600 12px inherit;color:#dbeafe;background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.22);border-radius:8px;padding:6px 10px;outline:none;cursor:pointer}
  .exp-select option{color:#0f172a}
  /* ---------- Hero ---------- */
  .hero{background:linear-gradient(118deg,var(--navy2) 0%,var(--blue) 58%,var(--cyan) 100%);
        color:#fff;padding:26px 30px 30px}
  .hero-in{max-width:1120px;margin:0 auto}
  .pill{display:inline-block;font-size:11px;font-weight:800;color:#0c2f6b;
        background:#bfdbfe;border-radius:999px;padding:4px 13px;margin-bottom:13px;letter-spacing:.3px}
  .hero h1{font-size:24px;font-weight:800;letter-spacing:.3px;line-height:1.25}
  .hero p{margin-top:9px;font-size:13px;line-height:1.7;color:#dbeafe;max-width:860px}
  /* ---------- 主体 ---------- */
  .shell{max-width:1120px;margin:0 auto;padding:18px 20px 34px}
  .cols{display:grid;grid-template-columns:1fr;gap:16px;align-items:start}
  @media (min-width:900px){.cols{grid-template-columns:minmax(300px,382px) 1fr}}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;
        padding:18px 20px;box-shadow:0 1px 3px rgba(15,23,42,.05)}
  h2{font-size:14px;font-weight:800;margin-bottom:15px;letter-spacing:.2px}

  /* ---------- 参数滑块 ---------- */
  .param{margin-bottom:14px}
  .param-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:6px}
  .param-label{font-size:12px;color:var(--dim)}
  .pnum{width:112px;padding:5px 9px;border-radius:8px;border:1px solid var(--line);
        font:600 12.5px Consolas,ui-monospace,monospace;text-align:right;
        background:#f8fafc;color:var(--ink);outline:none;transition:all .15s;-moz-appearance:textfield}
  .pnum::-webkit-outer-spin-button,.pnum::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
  .pnum:focus{border-color:#3b82f6;background:#fff;box-shadow:0 0 0 3px rgba(59,130,246,.15)}
  .pnum.bad{border-color:var(--err);box-shadow:0 0 0 3px rgba(220,38,38,.12)}
  .prange{-webkit-appearance:none;appearance:none;width:100%;height:5px;border-radius:999px;
          background:#e2e8f0;outline:none;cursor:pointer}
  .prange::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;
        background:var(--blue);border:2.5px solid #fff;box-shadow:0 1px 4px rgba(29,78,216,.45)}
  .prange::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:var(--blue);
        border:2.5px solid #fff;box-shadow:0 1px 4px rgba(29,78,216,.45)}
  .badge{margin-top:14px;font-size:11.5px;font-weight:700;padding:7px 12px;
         border-radius:9px;display:inline-block;line-height:1.4}
  .badge.good{background:#dcfce7;color:#15803d}
  .badge.okay{background:#dbeafe;color:#1d4ed8}
  .badge.warn{background:#fef3c7;color:#b45309}
  .badge.bad{background:#fee2e2;color:#b91c1c}
  .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:15px}
  .btn{-webkit-appearance:none;appearance:none;font:700 12.5px inherit;cursor:pointer;
       padding:9px 18px;border-radius:9px;color:#334155;background:#f1f5f9;
       border:1px solid var(--line);transition:all .15s}
  .btn:hover{background:#e2e8f0}
  .btn.blue{color:#fff;background:var(--blue);border-color:var(--blue);
            box-shadow:0 2px 8px rgba(29,78,216,.28)}
  .btn.blue:hover{background:#1e40af}

  /* ---------- KPI ---------- */
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));
        gap:10px;margin-bottom:17px}
  .kpi{border:1.5px solid #bfdbfe;border-radius:11px;padding:11px 13px;
       background:linear-gradient(180deg,#f8fbff,#fff)}
  .kpi .kl{font-size:10.5px;color:var(--dim);margin-bottom:6px;
           white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .kpi .kv{font:800 20px/1 "Segoe UI",system-ui,sans-serif;color:var(--blue);letter-spacing:-.4px}
  .kpi.hi{border-color:#99f6e4;background:linear-gradient(180deg,#f0fdfa,#fff)}
  .kpi.hi .kv{color:#0e7490}
  .kpi .ku{font-size:11px;font-weight:600;color:var(--dim);margin-left:4px;letter-spacing:0}

  /* ---------- 标签页 ---------- */
  .tabs{display:flex;gap:2px;border-bottom:1px solid var(--line);margin-bottom:15px;flex-wrap:wrap}
  .tab{border:0;background:none;font:700 12.5px inherit;color:var(--dim);cursor:pointer;
       padding:9px 15px;border-bottom:2px solid transparent;margin-bottom:-1px;transition:all .15s}
  .tab:hover{color:#334155}
  .tab.on{color:var(--blue);border-bottom-color:var(--blue)}
  .pane[hidden]{display:none}

  /* ---------- 明细 ---------- */
  .line{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
        padding:8px 0;border-bottom:1px solid #f1f5f9}
  .line:last-child{border-bottom:0}
  .line .k{font-size:12.5px;color:var(--dim)}
  .line .v{font:700 12.5px Consolas,ui-monospace,monospace;white-space:nowrap;text-align:right}
  .line .v.hi{color:var(--blue)}.line .v.ok{color:var(--ok)}
  .line .v.err{color:var(--err)}.line .v.warn{color:var(--warn)}
  .empty{font-size:12px;color:var(--faint);padding:14px 0}
  .note{margin-top:11px;font-size:11.5px;line-height:1.65;padding:10px 13px;border-radius:9px;
        color:var(--dim);background:#f8fafc;border-left:3px solid #94a3b8}
  .note.warn{color:#b45309;background:#fffbeb;border-left-color:var(--warn)}
  .note.err{color:#b91c1c;background:#fef2f2;border-left-color:var(--err)}

  canvas{width:100%;height:268px;display:block;touch-action:pan-y}

  /* ---------- 理论与主要公式 ---------- */
  .theory{margin-top:16px}
  .theory .theory-grid{display:grid;grid-template-columns:1fr;gap:10px}
  @media (min-width:780px){.theory .theory-grid{grid-template-columns:1fr 1fr}}
  .fm{display:flex;flex-direction:column;gap:5px;padding:10px 13px;border-radius:10px;
      background:#f8fafc;border:1px solid var(--line)}
  .fl{font-size:11px;color:var(--faint)}
  .fx{font:700 13px/1.55 Consolas,ui-monospace,monospace;color:var(--ink);
      word-break:break-word}
  .fx sub,.fx sup{font-size:9px;font-weight:700}
  .theory-note{margin-top:14px;font-size:12px;line-height:1.8;color:var(--dim);
               padding:11px 14px;border-radius:9px;background:#f8fafc;
               border-left:3px solid #93c5fd}
  .export{margin-top:16px;padding-top:14px;border-top:1px solid var(--line)}
  .export .hint{font-size:11px;color:var(--faint);margin-bottom:9px}
  textarea{width:100%;height:150px;margin-top:10px;padding:12px;border-radius:9px;resize:vertical;
    color:var(--ink);font:12px/1.6 Consolas,ui-monospace,monospace;
    background:#f8fafc;border:1px solid var(--line);outline:none}

  body.embed .hero{padding:18px 22px 20px}
  body.embed .hero h1{font-size:19px}
  body.embed .hero p{font-size:12px;margin-top:6px}
  body.embed .shell{padding:14px 16px 22px}
  body.embed .card{padding:15px 17px}
  body.embed .topbar{display:none}
  body.embed canvas{height:228px}
"""


# ============================================================
# 界面层 B
# ============================================================
UI = r"""
var TH = {
  grid:"#eef2f7", axis:"#cbd5e1", text:"#94a3b8",
  series:["#1d4ed8","#16a34a","#f59e0b","#dc2626","#7c3aed","#0891b2"],
  bar:[["#93c5fd","#1d4ed8"],["#5eead4","#0e7490"]],
  point:"#1d4ed8", mark:"#f59e0b"
};

/* ---------- 图表 ---------- */
function drawLegend(ctx, w, items){
  var x = w - 16;
  ctx.font = "11px system-ui,sans-serif";
  ctx.textAlign = "right"; ctx.textBaseline = "middle";
  var y = 14;
  items.forEach(function(it){
    var tw = ctx.measureText(it.label).width;
    ctx.fillStyle = "#f1f5f9"; ctx.strokeStyle = TH.axis; ctx.lineWidth = 0.5;
    var bw = tw + 30;
    ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x-bw, y-9, bw, 18, 9)
                                   : ctx.rect(x-bw, y-9, bw, 18);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = it.color || TH.series[0];
    ctx.beginPath(); ctx.arc(x-bw+10, y, 4, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = "#475569";
    ctx.fillText(it.label, x-4, y);
    x -= bw + 6;
  });
}

function drawBars(ctx, w, h, spec){
  var padL=58, padR=24, padT=44, padB=46;
  var x0=padL, x1=w-padR, y0=padT, y1=h-padB;
  var peak = 0;
  spec.bars.forEach(function(b){ if (b.value > peak) peak = b.value; });
  if (!(peak > 0)) peak = 1;
  var vmax = niceCeil(peak*1.18);
  var Y = function(v){ return y1 - (v/vmax)*(y1-y0); };

  ctx.font="10px Consolas,monospace"; ctx.textAlign="right"; ctx.textBaseline="middle";
  for (var i=0;i<=4;i++){
    var gv = vmax*i/4, gy = Y(gv);
    ctx.strokeStyle = i===0 ? TH.axis : TH.grid; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x0, gy+.5); ctx.lineTo(x1, gy+.5); ctx.stroke();
    ctx.fillStyle=TH.text; ctx.fillText(gv.toFixed(gv>=10?1:2), x0-9, gy);
  }
  ctx.save(); ctx.translate(14,(y0+y1)/2); ctx.rotate(-Math.PI/2);
  ctx.textAlign="center"; ctx.fillStyle=TH.text;
  ctx.font="11px system-ui,sans-serif"; ctx.fillText(spec.unit, 0, 0); ctx.restore();

  var slot=(x1-x0)/spec.bars.length, bw=Math.min(slot*0.34,100);
  spec.bars.forEach(function(b, idx){
    var cx = x0 + slot*(idx+0.5), top = Y(b.value);
    var col = TH.bar[idx % TH.bar.length], r = Math.min(bw/2, 8);
    var g = ctx.createLinearGradient(0, top, 0, y1);
    g.addColorStop(0, col[0]); g.addColorStop(1, col[1]);
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.moveTo(cx-bw/2, y1); ctx.lineTo(cx-bw/2, top+r);
    ctx.quadraticCurveTo(cx-bw/2, top, cx-bw/2+r, top);
    ctx.lineTo(cx+bw/2-r, top);
    ctx.quadraticCurveTo(cx+bw/2, top, cx+bw/2, top+r);
    ctx.lineTo(cx+bw/2, y1); ctx.closePath(); ctx.fill();
    ctx.fillStyle = "#0f172a"; ctx.font="700 13px Consolas,monospace";
    ctx.textAlign="center"; ctx.textBaseline="bottom";
    ctx.fillText(b.value.toFixed(b.value>=10?3:4), cx, top-8);
    ctx.fillStyle="#475569"; ctx.font="11.5px system-ui,sans-serif";
    ctx.textBaseline="top"; ctx.fillText(b.name, cx, y1+11);
  });
  drawLegend(ctx, w, spec.bars.map(function(b, i){
    return { label:b.name, color:TH.bar[i % TH.bar.length][1] };
  }));
}

function drawXY(ctx, w, h, spec){
  var padL=64, padR=26, padT=44, padB=52;
  var x0=padL, x1=w-padR, y0=padT, y1=h-padB;
  var xs=[], ys=[];
  spec.points.forEach(function(p){ xs.push(p[0]); ys.push(p[1]); });
  (spec.lines||[]).forEach(function(ln){ ln.points.forEach(function(p){ xs.push(p[0]); ys.push(p[1]); }); });
  (spec.marks||[]).forEach(function(m){ xs.push(m.x); ys.push(m.y); });
  var xmin=Math.min.apply(null,xs), xmax=Math.max.apply(null,xs);
  var ymin=Math.min.apply(null,ys), ymax=Math.max.apply(null,ys);
  var px=(xmax-xmin)*0.12 || Math.abs(xmax)*0.1 || 1;
  var py=(ymax-ymin)*0.16 || Math.abs(ymax)*0.1 || 1;
  xmin-=px; xmax+=px; ymin-=py; ymax+=py;

  var X=function(v){ return x0 + (v-xmin)/(xmax-xmin)*(x1-x0); };
  var Y=function(v){ return y1 - (v-ymin)/(ymax-ymin)*(y1-y0); };

  ctx.font="10px Consolas,monospace"; ctx.textAlign="right"; ctx.textBaseline="middle";
  for (var i=0;i<=4;i++){
    var gy = y0 + (y1-y0)*i/4;
    ctx.strokeStyle = i===4 ? TH.axis : TH.grid; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(x0, gy+.5); ctx.lineTo(x1, gy+.5); ctx.stroke();
    ctx.fillStyle=TH.text;
    ctx.fillText((ymax-(ymax-ymin)*i/4).toFixed(3), x0-9, gy);
  }
  ctx.textAlign="center"; ctx.textBaseline="top";
  for (var j=0;j<=3;j++){
    var gx = x0 + (x1-x0)*j/3;
    ctx.fillStyle=TH.text; ctx.fillText((xmin+(xmax-xmin)*j/3).toFixed(4), gx, y1+10);
  }
  ctx.fillStyle="#64748b"; ctx.font="11px system-ui,sans-serif";
  ctx.fillText(spec.xlabel, (x0+x1)/2, y1+28);
  ctx.save(); ctx.translate(16,(y0+y1)/2); ctx.rotate(-Math.PI/2);
  ctx.textBaseline="middle"; ctx.fillText(spec.ylabel, 0, 0); ctx.restore();

  (spec.lines||[]).forEach(function(ln, li){
    var col = ln.color || TH.series[(li+1) % TH.series.length];
    ctx.strokeStyle = col; ctx.lineWidth = 2.2;
    ctx.beginPath();
    ctx.moveTo(X(ln.points[0][0]), Y(ln.points[0][1]));
    ctx.lineTo(X(ln.points[1][0]), Y(ln.points[1][1]));
    ctx.stroke();
  });
  spec.points.forEach(function(p){
    ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 4, 0, Math.PI*2);
    ctx.fillStyle = "#fff"; ctx.fill();
    ctx.strokeStyle = TH.point; ctx.lineWidth = 2.2; ctx.stroke();
  });
  (spec.marks||[]).forEach(function(m){
    ctx.beginPath(); ctx.arc(X(m.x), Y(m.y), 6, 0, Math.PI*2);
    ctx.fillStyle = m.color || TH.mark; ctx.fill();
    ctx.strokeStyle="#fff"; ctx.lineWidth=2; ctx.stroke();
  });

  var items = [];
  spec.points.forEach(function(){ });
  (spec.lines||[]).forEach(function(ln, li){
    items.push({ label: ln.label || ("拟合线" + (li+1)),
                 color: ln.color || TH.series[(li+1) % TH.series.length] });
  });
  items.unshift({ label:"实验点", color:TH.point });
  (spec.marks||[]).forEach(function(){ items.push({ label:"理论极大", color:TH.mark }); });
  if (spec.legend && spec.legend.length) {
    var cols = [TH.point].concat((spec.lines||[]).map(function(ln, li){
      return ln.color || TH.series[(li+1) % TH.series.length]; })).concat([TH.mark]);
    items = spec.legend.map(function(l, i){ return { label:l.label, color:cols[i] || TH.series[i] }; });
  }
  drawLegend(ctx, w, items);
}

function drawChart(spec){
  var cv = document.getElementById("chart");
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var w = cv.clientWidth, h = cv.clientHeight;
  if (!w || !h) return;
  cv.width = Math.round(w*dpr); cv.height = Math.round(h*dpr);
  var ctx = cv.getContext("2d");
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,w,h);
  if (!spec){
    ctx.fillStyle="#cbd5e1"; ctx.font="13px system-ui,sans-serif";
    ctx.textAlign="center"; ctx.textBaseline="middle";
    ctx.fillText("暂无数据", w/2, h/2); return;
  }
  if (spec.kind === "bars") drawBars(ctx, w, h, spec);
  else drawXY(ctx, w, h, spec);
}

/* ---------- 页面 ---------- */
var EX = null, LAST = null, ENTRIES = {};

function el(tag, cls, text){
  var d = document.createElement(tag);
  if (cls) d.className = cls;
  if (text !== undefined) d.textContent = text;
  return d;
}

function buildParams(){
  var box = document.getElementById("params");
  box.innerHTML = ""; ENTRIES = {};
  EX.fields.forEach(function(f){
    var rg = RANGES[EX.id + "|" + f.key] || [0, (f.def || 1) * 2, "any"];
    var row = el("div","param");
    var top = el("div","param-top");
    top.appendChild(el("span","param-label", f.label + (f.unit ? "  (" + f.unit + ")" : "")));
    var num = document.createElement("input");
    num.type="number"; num.step="any"; num.className="pnum"; num.value=f.def;
    top.appendChild(num);
    row.appendChild(top);
    var rng = document.createElement("input");
    rng.type="range"; rng.className="prange";
    rng.min=rg[0]; rng.max=rg[1]; rng.step=rg[2]; rng.value=f.def;
    row.appendChild(rng);
    ENTRIES[f.key] = { num:num, rng:rng };
    rng.addEventListener("input", function(){ num.value = rng.value; doCalc(); });
    num.addEventListener("input", function(){ rng.value = num.value; doCalc(); });
    box.appendChild(row);
  });
}

function readInputs(){
  var v = {}, bad = [];
  EX.fields.forEach(function(f){
    var inp = ENTRIES[f.key].num;
    var raw = String(inp.value).trim();
    var n = raw === "" ? NaN : Number(raw);
    inp.classList.toggle("bad", !isFinite(n));
    if (!isFinite(n)) bad.push(f.label);
    v[f.key] = n;
  });
  return { v:v, bad:bad };
}

function renderKpis(list){
  var box = document.getElementById("kpis");
  box.innerHTML = "";
  if (!list || !list.length) return;
  list.forEach(function(k){
    var d = el("div","kpi" + (k.hi ? " hi" : ""));
    d.appendChild(el("div","kl", k.label));
    var v = el("div","kv", k.value);
    if (k.unit) v.appendChild(el("span","ku", k.unit));
    d.appendChild(v);
    box.appendChild(d);
  });
}

function renderRows(rows){
  var box = document.getElementById("rows");
  box.innerHTML = "";
  if (!rows.length){ box.appendChild(el("div","empty","正在计算…")); return; }
  rows.forEach(function(r){
    var line = el("div","line");
    line.appendChild(el("span","k", r.k));
    line.appendChild(el("span","v" + (r.cls ? " " + r.cls : ""), r.v));
    box.appendChild(line);
  });
}

function renderNotes(list){
  var box = document.getElementById("notes");
  box.innerHTML = "";
  (list||[]).forEach(function(n){
    box.appendChild(el("div","note " + (n.cls||""), n.text));
  });
}

function doCalc(){
  var r = readInputs();
  var badge = document.getElementById("badge");
  if (r.bad.length){
    LAST = null;
    renderKpis([]);
    renderRows([{ k:"请填写数字：" + r.bad.join("、"), v:"", cls:"err" }]);
    renderNotes([]); drawChart(null);
    badge.className = "badge bad"; badge.textContent = "参数不完整";
    return;
  }
  var out;
  try { out = EX.compute(r.v); }
  catch (e){ out = { err:"计算失败：" + (e && e.message ? e.message : e) }; }
  if (out.err){
    LAST = null;
    renderKpis([]);
    renderRows([{ k:out.err, v:"", cls:"err" }]);
    renderNotes([]); drawChart(null);
    badge.className = "badge bad"; badge.textContent = "数据异常";
    return;
  }
  LAST = out;
  renderKpis(out.kpis);
  renderRows(out.rows);
  renderNotes(out.notes);
  drawChart(out.chart);
  if (out.badge){
    badge.className = "badge " + (out.badge.cls || "okay");
    badge.textContent = out.badge.text;
  } else { badge.className = "badge okay"; badge.textContent = "已计算"; }
}

function doReset(){
  EX.fields.forEach(function(f){
    ENTRIES[f.key].num.value = f.def;
    ENTRIES[f.key].rng.value = f.def;
    ENTRIES[f.key].num.classList.remove("bad");
  });
  doCalc();
}

/* ---------- 导出 ---------- */
function plainText(){ return LAST ? LAST.plain.join("\r\n") : ""; }

function showPlain(){
  var ta = document.getElementById("plain");
  ta.hidden = false; ta.value = plainText(); ta.focus(); ta.select();
}

function copyResult(){
  if (!LAST){ renderNotes([{cls:"warn",text:"暂无可导出的结果。"}]); return; }
  var text = plainText();
  var ok = function(){ renderNotes([{cls:"",text:"已复制到剪贴板，可直接粘贴到实验报告。"}]); };
  var fail = function(){
    showPlain();
    renderNotes([{cls:"warn",text:"浏览器限制了剪贴板（需要 https），已把结果放在下方文本框，请手动 Ctrl+C。"}]);
  };
  if (navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(text).then(ok).catch(fail);
  } else {
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.cssText="position:fixed;top:-9999px";
    document.body.appendChild(ta); ta.select();
    var done = false;
    try { done = document.execCommand("copy"); } catch(e){ done = false; }
    document.body.removeChild(ta);
    done ? ok() : fail();
  }
}

function downloadCSV(){
  if (!LAST){ renderNotes([{cls:"warn",text:"暂无可导出的结果。"}]); return; }
  var v = readInputs().v;
  var rows = [[ "实验", EX.tag + " " + EX.name ],
              [ "导出时间", new Date().toLocaleString("zh-CN") ],
              [], [ "输入", "数值", "单位" ]];
  EX.fields.forEach(function(f){ rows.push([f.label, v[f.key], f.unit || ""]); });
  rows.push([]); rows.push([ "输出", "数值", "单位" ]);
  LAST.rows.forEach(function(r){
    var parts = String(r.v).split(" ");
    rows.push([ r.k, parts[0], parts.slice(1).join(" ") ]);
  });
  var csv = rows.map(function(line){
    return line.map(function(cell){
      var s = String(cell === undefined || cell === null ? "" : cell);
      return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g,'""') + '"' : s;
    }).join(",");
  }).join("\r\n");
  var blob = new Blob(["\ufeff" + csv], { type:"text/csv;charset=utf-8" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url; a.download = EX.tag.replace(/\s/g,"") + "_" + EX.name + ".csv";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(url); }, 3000);
  renderNotes([{cls:"",text:"CSV 已开始下载。若浏览器拦截了下载，可用「显示纯文本」手动复制。"}]);
}

/* ---------- 装载 ---------- */
function loadExp(i){
  EX = EXPS[i];
  document.getElementById("crumbName").textContent = EX.tag + " " + EX.name;
  document.getElementById("heroPill").textContent = EX.pill;
  document.getElementById("heroName").textContent = EX.name;
  document.getElementById("heroDesc").textContent = EX.desc;
  document.getElementById("theory").innerHTML = EX.theory || "";
  document.title = EX.name + " · 化学实验数据模拟器";
  var sel = document.getElementById("expSelect");
  if (sel) sel.value = String(i);
  buildParams();
  LAST = null;
  renderKpis([]); renderNotes([]); drawChart(null);
  doCalc();
  showPane("detail");
}

function showPane(name){
  var tabs = document.querySelectorAll(".tab");
  Array.prototype.forEach.call(tabs, function(t){
    t.classList.toggle("on", t.getAttribute("data-pane") === name);
  });
  document.getElementById("pane-detail").hidden = (name !== "detail");
  document.getElementById("pane-chart").hidden  = (name !== "chart");
  if (name === "chart" && LAST) drawChart(LAST.chart);
}

(function init(){
  if (new URLSearchParams(location.search).get("embed") === "1")
    document.body.classList.add("embed");

  var sel = document.getElementById("expSelect");
  if (EXPS.length > 1){
    EXPS.forEach(function(e, i){
      var o = document.createElement("option");
      o.value = String(i); o.textContent = e.tag + " " + e.name;
      sel.appendChild(o);
    });
    sel.addEventListener("change", function(){ loadExp(Number(sel.value)); });
  } else {
    sel.hidden = true;
  }

  document.getElementById("btnReset").addEventListener("click", doReset);
  document.getElementById("btnCopy").addEventListener("click", copyResult);
  document.getElementById("btnCsv").addEventListener("click", downloadCSV);
  document.getElementById("btnText").addEventListener("click", function(){
    if (!LAST){ return; }
    var ta = document.getElementById("plain");
    if (!ta.hidden){ ta.hidden = true; return; }
    showPlain();
  });
  Array.prototype.forEach.call(document.querySelectorAll(".tab"), function(t){
    t.addEventListener("click", function(){ showPane(t.getAttribute("data-pane")); });
  });
  if (window.ResizeObserver)
    new ResizeObserver(function(){ if (LAST) drawChart(LAST.chart); })
      .observe(document.getElementById("chart"));
  if (EXPS.length) loadExp(0);
})();
"""


# ============================================================
# 模板
# ============================================================
PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>@@TITLE@@</title>
<style>@@CSS@@</style>
</head>
<body>

<div class="topbar">
  <div class="crumb">
    化学实验数据处理 <i>›</i> 实验模拟器 <i>›</i> <b id="crumbName"></b>
  </div>
  <select class="exp-select" id="expSelect"></select>
</div>

<header class="hero">
  <div class="hero-in">
    <span class="pill" id="heroPill"></span>
    <h1 id="heroName"></h1>
    <p id="heroDesc"></p>
  </div>
</header>

<main class="shell">
  <div class="cols">
    <section class="card">
      <h2>参数设置</h2>
      <div id="params"></div>
      <div id="badge" class="badge okay"></div>
      <div class="row"><button class="btn" id="btnReset">重置为默认值</button></div>
    </section>

    <section class="card">
      <h2>计算结果</h2>
      <div class="kpis" id="kpis"></div>

      <div class="tabs">
        <button class="tab on" data-pane="detail">结果明细</button>
        <button class="tab" data-pane="chart">图表</button>
      </div>

      <div class="pane" id="pane-detail"><div id="rows"></div></div>
      <div class="pane" id="pane-chart" hidden><canvas id="chart"></canvas></div>

      <div id="notes"></div>

      <div class="export">
        <div class="hint">把结果填进实验报告：</div>
        <div class="row" style="margin-top:0">
          <button class="btn blue" id="btnCopy">复制结果</button>
          <button class="btn" id="btnCsv">下载 CSV</button>
          <button class="btn" id="btnText">显示纯文本</button>
        </div>
        <textarea id="plain" hidden readonly></textarea>
      </div>
    </section>
  </div>

  <section class="card theory">
    <h2>理论与主要公式</h2>
    <div id="theory"></div>
  </section>
</main>

<script>
"use strict";
/* ===== 实验定义（与版本 A 共用） ===== */
var EXPS = [@@DATA@@];
var RANGES = @@RANGES@@;
@@MATH@@
@@UI@@
</script>
</body>
</html>
"""


def js_exps(exps, single):
    if single:
        exps = [e for e in exps]
    out = []
    for e in exps:
        out.append(
            "{\n  id: %s,\n  tag: %s,\n  name: %s,\n  desc: %s,\n  pill: %s,\n"
            "  fields: %s,\n  theory: %s,\n  compute: %s\n}"
            % (js_str(e["file"]), js_str(e["tag"]), js_str(e["name"]),
               js_str(e["desc"]), js_str(PILL.get(e["file"], "")),
               js_fields(e["fields"]), js_str(e["theory"]), e["compute"]))
    return ",\n".join(out)


def js_ranges(exps):
    parts = []
    for e in exps:
        r = RANGES.get(e["file"], {})
        inner = ",".join('%s:[%s]' % (js_str(k), ",".join(repr(x) for x in v))
                         for k, v in r.items())
        parts.append("%s:{%s}" % (js_str(e["file"]), inner))
    return "{" + ",\n".join(parts) + "}"


def render_page(exps, title):
    return (PAGE
            .replace("@@TITLE@@", title)
            .replace("@@CSS@@", CSS)
            .replace("@@DATA@@", js_exps(exps, True))
            .replace("@@RANGES@@", js_ranges(exps))
            .replace("@@MATH@@", RUNTIME_MATH)
            .replace("@@UI@@", UI))


INDEX = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>化学实验数据模拟器 · 目录</title>
<style>
@@CSS@@
  .list{display:grid;grid-template-columns:1fr;gap:12px}
  @media (min-width:760px){.list{grid-template-columns:1fr 1fr}}
  .item{display:block;padding:15px 17px;border-radius:12px;text-decoration:none;color:inherit;
        background:#fff;border:1px solid var(--line);transition:all .15s}
  .item:hover{border-color:#93c5fd;box-shadow:0 8px 22px rgba(29,78,216,.10);transform:translateY(-2px)}
  .item .t{font-size:11px;font-weight:800;color:var(--cyan)}
  .item .n{display:block;font-size:15px;font-weight:800;margin:5px 0 4px}
  .item .d{font-size:11.5px;color:var(--dim);line-height:1.55}
</style>
</head>
<body>
<div class="topbar"><div class="crumb">化学实验数据处理 <i>›</i> <b>实验模拟器</b></div></div>
<header class="hero">
  <div class="hero-in">
    <span class="pill">模拟器库</span>
    <h1>化学实验数据模拟器</h1>
    <p>共 5 个实验。拖动参数即时查看计算结果，可导出文本或 CSV 填进实验报告。</p>
  </div>
</header>
<main class="shell">
  <div class="cols" style="grid-template-columns:1fr">
    <section class="card">
      <h2>实验列表</h2>
      <div class="list">@@ITEMS@@</div>
    </section>
    <section class="card">
      <h2>另有：单文件合并版</h2>
      <p style="font-size:12.5px;color:var(--dim);line-height:1.7">
        一个 HTML 里用下拉框切换全部 5 个实验 ——
        <a href="all-in-one.html" style="color:var(--blue);font-weight:800">打开 all-in-one.html →</a>
      </p>
    </section>
  </div>
</main>
@@WARN@@
</body>
</html>
"""


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    for e in EXPS:
        with open(os.path.join(OUT, e["file"] + ".html"), "w", encoding="utf-8") as f:
            f.write(render_page([e], e["name"] + " · 化学实验数据模拟器"))
        log("  生成 B/" + e["file"] + ".html")

    with open(os.path.join(OUT, "all-in-one.html"), "w", encoding="utf-8") as f:
        f.write(render_page(EXPS, "化学实验数据模拟器 · 5 个实验"))
    log("  生成 B/all-in-one.html")

    items = []
    for e in EXPS:
        items.append('<a class="item" href="%s.html">\n  <span class="t">%s · %s</span>\n'
                     '  <span class="n">%s</span>\n  <span class="d">%s</span>\n</a>'
                     % (e["file"], PILL.get(e["file"], ""), e["tag"], e["name"], e["desc"]))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.replace("@@CSS@@", CSS)
                     .replace("@@ITEMS@@", "\n".join(items))
                     .replace("@@WARN@@", WARN_JS))
    log("  生成 B/index.html")
    log("完成。")


if __name__ == "__main__":
    main()
