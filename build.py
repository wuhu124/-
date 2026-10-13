# -*- coding: utf-8 -*-
"""
化学实验数据处理系统 · 网页版生成器
======================================
一份模板 + 5 个实验定义 -> 生成：
  build/exp1..exp5.html     单实验页（可单独嵌入超星）
  build/all-in-one.html     单文件合并版（标签页切换 5 个实验）
  build/index.html          入口目录页
  build/部署说明.txt
  build/嵌入代码.txt
  build/本地预览.bat
输出全部为自包含单文件：零外部依赖、无 CDN、无构建步骤。

运行：python build.py
"""

import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build", "A")
PKG_NAME = "化学实验数据处理系统_网页版_v2.0"


def log(text):
    sys.stdout.write(text + "\n")


# ============================================================
# 配色：A · 清透浅色（Apple Liquid Glass 风）
# ============================================================
CSS = r"""
  :root{
    --ink:#0f172a; --dim:#475a70; --faint:#7a8ba3;
    --acc:#0369a1;  --acc2:#6d28d9;
    --ok:#047857;   --warn:#b45309;  --err:#be123c;
    --glass:linear-gradient(135deg,rgba(255,255,255,.76),rgba(255,255,255,.46));
    --stroke:rgba(255,255,255,.92);
    --shadow:0 10px 30px rgba(15,23,42,.10), inset 0 1px 0 #fff;
    --inputbg:rgba(255,255,255,.70); --inputbd:rgba(15,23,42,.11);
    --line:rgba(15,23,42,.085);
    --r:18px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{min-height:100%}
  body{
    font-family:"Microsoft YaHei UI","Microsoft YaHei","PingFang SC","Hiragino Sans GB",
                system-ui,-apple-system,"Segoe UI",sans-serif;
    color:var(--ink);
    background:linear-gradient(160deg,#eef3fa 0%,#dae6f6 48%,#e9eff8 100%);
    background-attachment:fixed;
    padding:20px; -webkit-font-smoothing:antialiased;
  }
  /* 背景柔光斑：玻璃卡片的"折射内容" */
  .bg{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none}
  .blob{position:absolute;border-radius:50%;filter:blur(64px);opacity:.5}
  .b1{width:42vw;height:42vw;left:-10vw;top:-12vw;background:#60a5fa}
  .b2{width:34vw;height:34vw;right:-8vw;top:-8vw;background:#f0abfc;opacity:.38}
  .b3{width:40vw;height:40vw;right:-6vw;bottom:-16vw;background:#5eead4;opacity:.42}
  .b4{width:30vw;height:30vw;left:-6vw;bottom:-12vw;background:#c7d2fe;opacity:.55}
  .blob{animation:float 20s ease-in-out infinite alternate}
  .b2{animation-duration:24s}.b3{animation-duration:28s}.b4{animation-duration:32s}
  @keyframes float{from{transform:translate3d(0,0,0)}to{transform:translate3d(2.5vw,1.8vw,0)}}
  @media (prefers-reduced-motion:reduce){.blob{animation:none}}

  .wrap{max-width:1080px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
  .card{
    background:var(--glass);
    -webkit-backdrop-filter:blur(22px) saturate(180%);
    backdrop-filter:blur(22px) saturate(180%);
    border:1px solid var(--stroke); border-radius:var(--r);
    box-shadow:var(--shadow); padding:18px 20px;
  }
  /* 老内核不支持 backdrop-filter 时，退化成半透明纯色，绝不糊成一团 */
  @supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
    .card{background:rgba(255,255,255,.93)}
  }

  h1{font-size:18px;font-weight:700;letter-spacing:.2px}
  h2{font-size:13px;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:12px}
  h2::before{content:"";width:3px;height:13px;border-radius:2px;
             background:linear-gradient(180deg,#38bdf8,#6d28d9)}
  .sub{font-size:12px;color:var(--dim);margin-top:5px;line-height:1.55}
  .head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
  .tag{flex:none;font-size:11px;font-weight:700;color:var(--acc2);
       padding:4px 11px;border-radius:999px;white-space:nowrap;
       background:rgba(109,40,217,.09);border:1px solid rgba(109,40,217,.22)}

  /* 标签页（仅合并版显示） */
  .tabs{display:flex;gap:8px;flex-wrap:wrap}
  .tab{
    font:600 12.5px/1 inherit;padding:9px 15px;border-radius:999px;cursor:pointer;
    color:var(--dim);background:rgba(255,255,255,.55);
    border:1px solid rgba(255,255,255,.9);transition:all .16s;
  }
  .tab:hover{background:rgba(255,255,255,.8)}
  .tab.on{color:#fff;background:linear-gradient(135deg,#0369a1,#4338ca);
          border-color:transparent;box-shadow:0 4px 14px rgba(3,105,161,.28)}

  .cols{display:grid;grid-template-columns:1fr;gap:16px;align-items:start}
  @media (min-width:860px){.cols{grid-template-columns:minmax(280px,380px) 1fr}}

  .grid{display:grid;grid-template-columns:1fr;gap:11px}
  label{display:flex;flex-direction:column;gap:5px;font-size:12px;color:var(--dim)}
  .unit{color:var(--faint);font-size:11px}
  input[type=number]{
    width:100%;padding:9px 12px;border-radius:10px;color:var(--ink);
    font:600 14px/1.2 Consolas,ui-monospace,monospace;text-align:right;
    background:var(--inputbg);border:1px solid var(--inputbd);outline:none;
    transition:border-color .15s,box-shadow .15s;-moz-appearance:textfield;
  }
  input[type=number]::-webkit-outer-spin-button,
  input[type=number]::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
  input[type=number]:focus{border-color:#0284c7;box-shadow:0 0 0 3px rgba(2,132,199,.16)}
  input.bad{border-color:#be123c;box-shadow:0 0 0 3px rgba(190,18,60,.14)}

  .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:15px}
  .btn{-webkit-appearance:none;appearance:none;font-family:inherit;cursor:pointer;
    font-size:13px;font-weight:700;padding:10px 22px;border-radius:999px;
    color:var(--ink);background:rgba(255,255,255,.62);
    border:1px solid rgba(15,23,42,.14);transition:all .16s}
  .btn:hover{background:#fff;transform:translateY(-1px);box-shadow:0 6px 16px rgba(15,23,42,.10)}
  .btn:active{transform:translateY(0) scale(.985)}
  .btn.primary{color:#fff;border-color:transparent;
    background:linear-gradient(135deg,#0369a1,#4338ca);
    box-shadow:0 6px 18px rgba(3,105,161,.30)}
  .btn.primary:hover{box-shadow:0 10px 24px rgba(3,105,161,.38)}
  .btn.sm{padding:7px 15px;font-size:12px;font-weight:600}

  .res{display:flex;flex-direction:column}
  .line{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
        padding:7px 2px;border-bottom:1px solid var(--line)}
  .line:last-child{border-bottom:0}
  .k{font-size:12px;color:var(--dim)}
  .v{font:700 14px/1.3 Consolas,ui-monospace,monospace;text-align:right;white-space:nowrap}
  .v.ok{color:var(--ok)}.v.err{color:var(--err)}.v.warn{color:var(--warn)}
  .v.hi{color:var(--acc)}
  .empty{font-size:12px;color:var(--faint);padding:14px 2px}

  .chart-box{margin-top:14px}
  canvas{width:100%;height:240px;display:block;border-radius:12px;touch-action:pan-y}

  .note{margin-top:12px;font-size:11.5px;line-height:1.65;color:var(--dim);
        padding:10px 13px;border-radius:10px;
        background:rgba(255,255,255,.55);border-left:3px solid #0284c7}
  .note.warn{color:var(--warn);border-left-color:var(--warn);background:rgba(180,83,9,.07)}
  .note.err{color:var(--err);border-left-color:var(--err);background:rgba(190,18,60,.07)}

  .export{margin-top:14px;padding-top:13px;border-top:1px solid var(--line)}
  .export .hint{font-size:11px;color:var(--faint);margin-bottom:9px}
  textarea{width:100%;height:150px;margin-top:10px;padding:12px;border-radius:10px;
    resize:vertical;color:var(--ink);font:12px/1.6 Consolas,ui-monospace,monospace;
    background:rgba(255,255,255,.75);border:1px solid var(--inputbd);outline:none}
  footer{text-align:center;font-size:11px;color:var(--faint);padding:2px 0 6px}

  /* ---------- 理论与主要公式 ---------- */
  .theory .theory-grid{display:grid;grid-template-columns:1fr;gap:10px}
  @media (min-width:780px){.theory .theory-grid{grid-template-columns:1fr 1fr}}
  .fm{display:flex;flex-direction:column;gap:5px;padding:10px 13px;border-radius:11px;
      background:rgba(255,255,255,.62);border:1px solid rgba(255,255,255,.9)}
  .fl{font-size:11px;color:var(--faint)}
  .fx{font:600 13px/1.55 Consolas,ui-monospace,monospace;color:var(--ink);
      word-break:break-word}
  .fx sub,.fx sup{font-size:9px;font-weight:600}
  .theory-note{margin-top:13px;font-size:11.5px;line-height:1.75;color:var(--dim);
               padding-left:11px;border-left:2px solid rgba(2,132,199,.35)}

  body.embed{padding:12px}
  body.embed .wrap{gap:12px}
  body.embed .card{padding:15px 17px;border-radius:15px}
  body.embed h1{font-size:16px}
  body.embed canvas{height:196px}
  body.embed footer{display:none}
"""


# ============================================================
# 运行时 JS（插值 / 拟合 / 渲染 / 图表 / 导出 / 标签页）
# ============================================================
RUNTIME_MATH = r"""
var REF = { Mg_M:24.305, HAc_Ka:1.8e-5, BaSO4_Ksp:1.1e-10, Ea:51.8, R:8.314 };

var WATER_VP = { 273.15:610.6, 278.15:872.0, 283.15:1228.1, 288.15:1705.0,
                 293.15:2338.8, 298.15:3167.2, 303.15:4242.8, 308.15:5622.9 };
var BASO4_LAMBDA0 = { 288.15:2.798e-2, 293.15:2.991e-2,
                      298.15:2.8688e-2, 303.15:3.134e-2 };

/* ---------- 数学 ---------- */
function interp(T, table){
  var keys = Object.keys(table).map(Number).sort(function(a,b){return a-b;});
  if (T <= keys[0]) return table[String(keys[0])];
  var last = keys[keys.length-1];
  if (T >= last) return table[String(last)];
  for (var i=0;i<keys.length-1;i++){
    var a=keys[i], b=keys[i+1];
    if (T>=a && T<=b) return table[String(a)] + (table[String(b)]-table[String(a)])*(T-a)/(b-a);
  }
  return table[String(last)];
}
function rangeNote(T, table, name){
  var keys = Object.keys(table).map(Number).sort(function(a,b){return a-b;});
  var lo = keys[0], hi = keys[keys.length-1];
  if (T < lo || T > hi) return [{ cls:"warn", text:"温度 T = " + T + " K 超出" + name
      + "数据范围 " + lo + " ~ " + hi + " K，已按最近端点值处理，结果仅供参考。" }];
  return [];
}
function linfit(xs, ys){
  var n = xs.length, sx=0, sy=0, sxx=0, sxy=0;
  for (var i=0;i<n;i++){ sx+=xs[i]; sy+=ys[i]; sxx+=xs[i]*xs[i]; sxy+=xs[i]*ys[i]; }
  var d = n*sxx - sx*sx;
  if (d === 0) return null;
  var k = (n*sxy - sx*sy)/d;
  return [k, (sy - k*sx)/n];
}
function fmtE(x, d){
  if (d === undefined) d = 3;
  return x.toExponential(d).replace(/e([+-])(\d)$/, "e$10$2");
}
function niceCeil(x){
  var mag = Math.pow(10, Math.floor(Math.log(x)/Math.LN10));
  var steps = [1,1.5,2,2.5,3,4,5,6,8,10];
  for (var i=0;i<steps.length;i++) if (x <= steps[i]*mag) return steps[i]*mag;
  return 10*mag;
}
"""


# ============================================================
# 界面层 A：清透玻璃版
# ============================================================
RUNTIME_UI = r"""
/* ---------- 主题色（浅色） ---------- */
var TH = {
  ink:"#0f172a", dim:"#7a8ba3", grid:"rgba(15,23,42,.085)",
  axis:"rgba(15,23,42,.22)", bar:[["#7dd3fc","#0284c7"],["#c4b5fd","#6d28d9"]],
  point:"#0284c7", line1:"#0284c7", line2:"#0f766e", mark:"#b45309"
};

/* ---------- 图表 ---------- */
function drawBars(ctx, w, h, spec){
  var padL=56, padR=24, padT=24, padB=48;
  var x0=padL, x1=w-padR, y0=padT, y1=h-padB;
  var peak = 0;
  spec.bars.forEach(function(b){ if (b.value > peak) peak = b.value; });
  if (!(peak > 0)) peak = 1;
  var vmax = niceCeil(peak*1.18);
  var Y = function(v){ return y1 - (v/vmax)*(y1-y0); };

  ctx.font = "10px Consolas,monospace"; ctx.textAlign="right"; ctx.textBaseline="middle";
  for (var i=0;i<=4;i++){
    var gv = vmax*i/4, gy = Y(gv);
    ctx.strokeStyle = i===0 ? TH.axis : TH.grid; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x0, gy+.5); ctx.lineTo(x1, gy+.5); ctx.stroke();
    ctx.fillStyle = TH.dim;
    ctx.fillText(gv.toFixed(gv>=10?1:2), x0-9, gy);
  }
  ctx.save(); ctx.translate(14,(y0+y1)/2); ctx.rotate(-Math.PI/2);
  ctx.textAlign="center"; ctx.fillStyle=TH.dim;
  ctx.font="11px system-ui,sans-serif"; ctx.fillText(spec.unit, 0, 0); ctx.restore();

  var slot = (x1-x0)/spec.bars.length, bw = Math.min(slot*0.36, 96);
  spec.bars.forEach(function(b, idx){
    var cx = x0 + slot*(idx+0.5);
    var top = Y(b.value);
    var col = TH.bar[idx % TH.bar.length];
    var r = Math.min(bw/2, 11);
    var g = ctx.createLinearGradient(0, top, 0, y1);
    g.addColorStop(0, col[0]); g.addColorStop(1, col[1]);
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.moveTo(cx-bw/2, y1); ctx.lineTo(cx-bw/2, top+r);
    ctx.quadraticCurveTo(cx-bw/2, top, cx-bw/2+r, top);
    ctx.lineTo(cx+bw/2-r, top);
    ctx.quadraticCurveTo(cx+bw/2, top, cx+bw/2, top+r);
    ctx.lineTo(cx+bw/2, y1); ctx.closePath(); ctx.fill();

    ctx.fillStyle = TH.ink; ctx.font = "700 12px Consolas,monospace";
    ctx.textAlign="center"; ctx.textBaseline="bottom";
    var d = b.value>=100 ? 2 : b.value>=10 ? 2 : 3;
    ctx.fillText(b.value.toFixed(d), cx, top-9);

    ctx.fillStyle = "#475a70"; ctx.font = "11.5px system-ui,sans-serif";
    ctx.textBaseline="top"; ctx.fillText(b.name, cx, y1+11);
  });
}

function drawXY(ctx, w, h, spec){
  var padL=62, padR=26, padT=26, padB=52;
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

  var X = function(v){ return x0 + (v-xmin)/(xmax-xmin)*(x1-x0); };
  var Y = function(v){ return y1 - (v-ymin)/(ymax-ymin)*(y1-y0); };

  ctx.font="10px Consolas,monospace"; ctx.textAlign="right"; ctx.textBaseline="middle";
  for (var i=0;i<=4;i++){
    var gv = ymin + (ymax-ymin)*i/4, gy = Y(gv);
    ctx.strokeStyle = i===0 ? TH.axis : TH.grid; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(x0, gy+.5); ctx.lineTo(x1, gy+.5); ctx.stroke();
    ctx.fillStyle=TH.dim; ctx.fillText(gv.toFixed(3), x0-9, gy);
  }
  ctx.textAlign="center"; ctx.textBaseline="top";
  for (var j=0;j<=3;j++){
    var gx = x0 + (x1-x0)*j/3;
    ctx.fillStyle=TH.dim; ctx.fillText((xmin+(xmax-xmin)*j/3).toFixed(4), gx, y1+10);
  }
  ctx.fillStyle="#475a70"; ctx.font="11px system-ui,sans-serif";
  ctx.textAlign="center"; ctx.textBaseline="top";
  ctx.fillText(spec.xlabel, (x0+x1)/2, y1+28);
  ctx.save(); ctx.translate(16,(y0+y1)/2); ctx.rotate(-Math.PI/2);
  ctx.textBaseline="middle"; ctx.fillText(spec.ylabel, 0, 0); ctx.restore();

  var colors=[TH.line1, TH.line2];
  (spec.lines||[]).forEach(function(ln, li){
    var col = ln.color || colors[li % colors.length];
    ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.globalAlpha = .9;
    ctx.beginPath();
    ctx.moveTo(X(ln.points[0][0]), Y(ln.points[0][1]));
    ctx.lineTo(X(ln.points[1][0]), Y(ln.points[1][1]));
    ctx.stroke(); ctx.globalAlpha = 1;
  });
  spec.points.forEach(function(p){
    ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 3.4, 0, Math.PI*2);
    ctx.fillStyle = "#fff"; ctx.fill();
    ctx.strokeStyle = TH.point; ctx.lineWidth = 2; ctx.stroke();
  });
  (spec.marks||[]).forEach(function(m){
    ctx.beginPath(); ctx.arc(X(m.x), Y(m.y), 5.5, 0, Math.PI*2);
    ctx.fillStyle = m.color || TH.mark; ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.6; ctx.stroke();
  });
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
    ctx.fillStyle = "rgba(15,23,42,.22)"; ctx.font="13px system-ui,sans-serif";
    ctx.textAlign="center"; ctx.textBaseline="middle";
    ctx.fillText("暂无数据", w/2, h/2); return;
  }
  if (spec.kind === "bars") drawBars(ctx, w, h, spec);
  else drawXY(ctx, w, h, spec);
}

/* ---------- 页面状态 ---------- */
var EX = null, LAST = null, ENTRIES = {};

function el(tag, cls, text){
  var d = document.createElement(tag);
  if (cls) d.className = cls;
  if (text !== undefined) d.textContent = text;
  return d;
}

function buildForm(){
  var box = document.getElementById("fields");
  box.innerHTML = "";
  ENTRIES = {};
  var grid = el("div","grid");
  EX.fields.forEach(function(f){
    var lab = el("label");
    lab.appendChild(document.createTextNode(f.label));
    if (f.unit) lab.appendChild(el("span","unit",f.unit));
    var inp = document.createElement("input");
    inp.type = "number"; inp.step = "any"; inp.value = f.def;
    inp.addEventListener("keydown", function(e){
      if (e.key === "Enter"){ e.preventDefault(); doCalc(); }
    });
    ENTRIES[f.key] = inp;
    lab.appendChild(inp);
    grid.appendChild(lab);
  });
  box.appendChild(grid);
}

function readInputs(){
  var v = {}, bad = [];
  EX.fields.forEach(function(f){
    var inp = ENTRIES[f.key];
    var raw = String(inp.value).trim();
    var n = raw === "" ? NaN : Number(raw);
    inp.classList.toggle("bad", !isFinite(n));
    if (!isFinite(n)) bad.push(f.label);
    v[f.key] = n;
  });
  return { v:v, bad:bad };
}

function render(rows){
  var box = document.getElementById("results");
  box.innerHTML = "";
  if (!rows.length){ box.appendChild(el("div","empty","点击「计算」查看结果")); return; }
  rows.forEach(function(r){
    var line = el("div","line");
    line.appendChild(el("span","k", r.k));
    var v = el("span","v" + (r.cls ? " " + r.cls : ""), r.v);
    line.appendChild(v);
    box.appendChild(line);
  });
}

function notes(arr){
  var box = document.getElementById("msg");
  box.innerHTML = "";
  (arr||[]).forEach(function(n){
    box.appendChild(el("div","note " + (n.cls||""), n.text));
  });
}

function doCalc(){
  var r = readInputs();
  if (r.bad.length){
    LAST = null;
    render([{k:"请填写数字：" + r.bad.join("、"), v:"", cls:"err"}]);
    notes([]); drawChart(null); return;
  }
  var out;
  try { out = EX.compute(r.v); }
  catch (e){ out = { err:"计算失败：" + (e && e.message ? e.message : e) }; }
  if (out.err){
    LAST = null;
    render([{k:out.err, v:"", cls:"err"}]);
    notes([]); drawChart(null); return;
  }
  LAST = out;
  render(out.rows);
  notes(out.notes);
  drawChart(out.chart);
}

function doReset(){
  EX.fields.forEach(function(f){
    ENTRIES[f.key].value = f.def;
    ENTRIES[f.key].classList.remove("bad");
  });
  LAST = null; render([]); notes([]); drawChart(null);
}

/* ---------- 导出 ---------- */
function plainText(){ return LAST ? LAST.plain.join("\r\n") : ""; }

function showPlain(){
  var ta = document.getElementById("plain");
  ta.hidden = false; ta.value = plainText(); ta.focus(); ta.select();
}

function copyResult(){
  if (!LAST){ notes([{cls:"warn",text:"请先点「计算」。"}]); return; }
  var text = plainText();
  var ok = function(){ notes([{cls:"",text:"已复制到剪贴板，可直接粘贴到实验报告。"}]); };
  var fail = function(){
    showPlain();
    notes([{cls:"warn",text:"浏览器限制了剪贴板（需要 https），已把结果放在下面的文本框，请手动 Ctrl+C 复制。"}]);
  };
  if (navigator.clipboard && window.isSecureContext){
    navigator.clipboard.writeText(text).then(ok).catch(fail);
  } else {
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.cssText = "position:fixed;top:-9999px";
    document.body.appendChild(ta); ta.select();
    var done = false;
    try { done = document.execCommand("copy"); } catch (e){ done = false; }
    document.body.removeChild(ta);
    done ? ok() : fail();
  }
}

function downloadCSV(){
  if (!LAST){ notes([{cls:"warn",text:"请先点「计算」。"}]); return; }
  var v = readInputs().v;
  var rows = [[ "实验", EX.tag + " " + EX.name ],
              [ "导出时间", new Date().toLocaleString("zh-CN") ],
              [],
              [ "输入", "数值", "单位" ]];
  EX.fields.forEach(function(f){ rows.push([f.label, v[f.key], f.unit || ""]); });
  rows.push([]);
  rows.push([ "输出", "数值", "单位" ]);
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
  notes([{cls:"",text:"CSV 已开始下载。若浏览器拦截了下载，可用「显示纯文本」手动复制。"}]);
}

/* ---------- 装载 ---------- */
function loadExp(i){
  EX = EXPS[i];
  document.getElementById("expName").textContent = EX.name;
  document.getElementById("expDesc").textContent = EX.desc;
  document.getElementById("expTag").textContent = EX.tag;
  document.getElementById("theory").innerHTML = EX.theory || "";
  document.title = EX.name + " · 化学实验数据处理";
  document.getElementById("footer").textContent =
    "化学实验常数测定数据处理 · " + EX.tag + " · " + EX.name;
  var tabs = document.getElementById("tabs");
  Array.prototype.forEach.call(tabs.children, function(t, k){
    t.classList.toggle("on", k === i);
  });
  buildForm();
  LAST = null;
  render([]); notes([]); drawChart(null);
  doCalc();
}

(function init(){
  if (new URLSearchParams(location.search).get("embed") === "1")
    document.body.classList.add("embed");

  var tabs = document.getElementById("tabs");
  if (EXPS.length > 1){
    EXPS.forEach(function(e, i){
      var t = el("button","tab", e.tag + " " + e.name);
      t.addEventListener("click", function(){ loadExp(i); });
      tabs.appendChild(t);
    });
  } else {
    tabs.hidden = true;
  }
  document.getElementById("btnCalc").addEventListener("click", doCalc);
  document.getElementById("btnReset").addEventListener("click", doReset);
  document.getElementById("btnCopy").addEventListener("click", copyResult);
  document.getElementById("btnCsv").addEventListener("click", downloadCSV);
  document.getElementById("btnText").addEventListener("click", function(){
    if (!LAST){ notes([{cls:"warn",text:"请先点「计算」。"}]); return; }
    var ta = document.getElementById("plain");
    if (!ta.hidden){ ta.hidden = true; return; }
    showPlain();
  });
  if (window.ResizeObserver)
    new ResizeObserver(function(){ if (LAST) drawChart(LAST.chart); })
      .observe(document.getElementById("chart"));
  if (EXPS.length) loadExp(0);
})();
"""

RUNTIME = RUNTIME_MATH + RUNTIME_UI


# ============================================================
# 5 个实验定义
# ============================================================
EXPS = []

EXPS.append({
    "file": "exp1-mg-molar-mass",
    "tag": "表 3-1",
    "name": "量气法测定镁的摩尔质量",
    "desc": "由镁与稀硫酸反应放出的氢气体积，按理想气体状态方程求 M(Mg)",
    "fields": [
        {"key": "m",  "label": "镁条质量 m",    "unit": "mg", "def": 25.0},
        {"key": "v1", "label": "反应前读数 V₁", "unit": "mL", "def": 0.0},
        {"key": "v2", "label": "反应后读数 V₂", "unit": "mL", "def": 22.5},
        {"key": "p",  "label": "大气压 p",      "unit": "Pa", "def": 101325},
        {"key": "t",  "label": "室温 T",        "unit": "K",  "def": 298.15},
    ],
    "compute": r"""
function (v) {
  if (!(v.m > 0))     return { err:"镁条质量 m 必须大于 0" };
  if (!(v.t > 0))     return { err:"室温 T 必须大于 0" };
  if (!(v.p > 0))     return { err:"大气压 p 必须大于 0" };
  if (!(v.v2 > v.v1)) return { err:"反应后读数 V₂ 必须大于 V₁（气体体积为正）" };
  var p_h2o = interp(v.t, WATER_VP);
  var p_h2  = v.p - p_h2o;
  if (!(p_h2 > 0)) return { err:"大气压必须大于该温度下水的饱和蒸气压" };
  var dV = v.v2 - v.v1;
  var M   = v.m*1e-6 * REF.R * v.t / (p_h2 * dV*1e-6) * 1e3;
  var err = Math.abs(M - REF.Mg_M) / REF.Mg_M * 100;
  var notes = rangeNote(v.t, WATER_VP, "水饱和蒸气压");
  return {
    notes: notes,
    kpis: [
      { label:"气体体积 V",     value: dV.toFixed(2),   unit:"mL" },
      { label:"氢气分压 p(H₂)", value: p_h2.toFixed(0), unit:"Pa" },
      { label:"摩尔质量 M(Mg)", value: M.toFixed(3),    unit:"g/mol", hi:1 },
      { label:"相对误差",       value: err.toFixed(2),  unit:"%" }
    ],
    badge: { cls: notes.length ? "warn" : "good",
             text: "室温 " + v.t + " K · 氢气分压 " + p_h2.toFixed(0) + " Pa" },
    rows: [
      { k:"气体体积 V",          v: dV.toFixed(2) + " mL" },
      { k:"水饱和蒸气压 p(H₂O)", v: p_h2o.toFixed(2) + " Pa" },
      { k:"氢气分压 p(H₂)",      v: p_h2.toFixed(2) + " Pa" },
      { k:"摩尔质量 M(Mg)",      v: M.toFixed(3) + " g/mol", cls:"hi" },
      { k:"相对误差",            v: err.toFixed(2) + " %" }
    ],
    chart: { kind:"bars", unit:"g/mol", bars:[
      { name:"测量值", value:M },
      { name:"理论值", value:REF.Mg_M }
    ]},
    plain: [
      "表 3-1  量气法测定镁的摩尔质量",
      "镁条质量 m = " + v.m + " mg",
      "反应前读数 V1 = " + v.v1 + " mL",
      "反应后读数 V2 = " + v.v2 + " mL",
      "大气压 p = " + v.p + " Pa",
      "室温 T = " + v.t + " K",
      "----------------------------------",
      "气体体积 V = " + dV.toFixed(2) + " mL",
      "水饱和蒸气压 p(H2O) = " + p_h2o.toFixed(2) + " Pa",
      "氢气分压 p(H2) = " + p_h2.toFixed(2) + " Pa",
      "摩尔质量 M(Mg) = " + M.toFixed(3) + " g/mol",
      "相对误差 = " + err.toFixed(2) + " %"
    ]
  };
}
""",
})

EXPS.append({
    "file": "exp2-acetic-ka",
    "tag": "表 3-2",
    "name": "pH 法测乙酸电离常数",
    "desc": "配制 4 份不同浓度的乙酸溶液，测 pH 后求电离常数 Ka",
    "fields": [
        {"key": "c0",  "label": "乙酸标准浓度 c₀", "unit": "mol/L", "def": 0.1},
        {"key": "ph1", "label": "1 号溶液 pH", "unit": "", "def": 3.50},
        {"key": "ph2", "label": "2 号溶液 pH", "unit": "", "def": 3.20},
        {"key": "ph3", "label": "3 号溶液 pH", "unit": "", "def": 2.90},
        {"key": "ph4", "label": "4 号溶液 pH", "unit": "", "def": 2.70},
    ],
    "compute": r"""
function (v) {
  if (!(v.c0 > 0)) return { err:"乙酸标准浓度 c₀ 必须大于 0" };
  var VOL = [[3,45],[6,42],[12,36],[24,24]];
  var kas = [], rows = [], lastF = "式3-6", maxAl = 0;
  var plain = ["表 3-2  pH 法测乙酸电离常数", "c0 = " + v.c0 + " mol/L"];
  for (var i=0;i<4;i++){
    var ph = v["ph" + (i+1)];
    if (!isFinite(ph)) return { err:(i+1) + " 号溶液 pH 无效" };
    var c  = v.c0 * VOL[i][0] / (VOL[i][0] + VOL[i][1]);
    var h  = Math.pow(10, -ph);
    var al = h / c * 100;
    var ka = al < 5 ? h*h/c : h*h/(c-h);
    var f  = al < 5 ? "式3-8" : "式3-6";
    kas.push(ka);
    lastF = f;
    if (al > maxAl) maxAl = al;
    rows.push({ k:(i+1) + " 号溶液  c=" + c.toFixed(5) + " α=" + al.toFixed(2) + "%  " + f,
                v: fmtE(ka) });
    plain.push((i+1) + " 号溶液  c = " + c.toFixed(5) + " mol/L  α = " + al.toFixed(2)
               + "%  Ka = " + fmtE(ka) + "  (" + f + ")");
  }
  var avg = 0;
  kas.forEach(function(x){ avg += x; });
  avg /= kas.length;
  var err = Math.abs(avg - REF.HAc_Ka) / REF.HAc_Ka * 100;
  rows.push({ k:"Ka 平均值", v: fmtE(avg), cls:"hi" });
  rows.push({ k:"相对误差",  v: err.toFixed(2) + " %" });
  plain.push("----------------------------------");
  plain.push("Ka 平均 = " + fmtE(avg) + "  (理论 " + fmtE(REF.HAc_Ka, 1) + ")");
  plain.push("相对误差 = " + err.toFixed(2) + " %");
  return {
    notes: [],
    rows: rows,
    kpis: [
      { label:"Ka 平均值",    value: fmtE(avg),        unit:"mol/L", hi:1 },
      { label:"相对误差",     value: err.toFixed(2),   unit:"%" },
      { label:"最大电离度 α", value: maxAl.toFixed(2), unit:"%" },
      { label:"样品数",       value: "4",              unit:"份" }
    ],
    badge: { cls:"okay", text:"最大 α = " + maxAl.toFixed(2) + "% → 采用 " + lastF },
    chart: { kind:"bars", unit:"×10⁻⁵", bars:[
      { name:"测量值", value: avg * 1e5 },
      { name:"理论值", value: REF.HAc_Ka * 1e5 }
    ]},
    plain: plain
  };
}
""",
})

EXPS.append({
    "file": "exp3-baso4-ksp",
    "tag": "表 3-3",
    "name": "电导法测 BaSO₄ 溶度积",
    "desc": "由 BaSO₄ 饱和溶液的电导率求溶解度与溶度积 Ksp",
    "fields": [
        {"key": "cw", "label": "去离子水电导率 χ(H₂O)",  "unit": "μS/cm", "def": 1.5},
        {"key": "cs", "label": "饱和溶液电导率 χ(溶液)", "unit": "μS/cm", "def": 4.0},
        {"key": "t",  "label": "实验温度 T",             "unit": "K",    "def": 298.15},
    ],
    "compute": r"""
function (v) {
  if (!(v.t > 0)) return { err:"实验温度 T 必须大于 0" };
  var d = (v.cs - v.cw) * 1e-4;
  if (!(d > 0)) return { err:"χ(溶液) 必须大于 χ(H₂O)，否则 BaSO₄ 的贡献为负，请检查测量值" };
  var lam0 = interp(v.t, BASO4_LAMBDA0);
  var c    = d / lam0 / 1000;
  var ksp  = c * c;
  var err  = Math.abs(ksp - REF.BaSO4_Ksp) / REF.BaSO4_Ksp * 100;
  var notes = rangeNote(v.t, BASO4_LAMBDA0, "BaSO₄ 极限摩尔电导率");
  return {
    notes: notes,
    kpis: [
      { label:"λ₀(BaSO₄)", value: fmtE(lam0, 4),    unit:"S·m²/mol" },
      { label:"溶解度 c",   value: fmtE(c, 4),       unit:"mol/L" },
      { label:"溶度积 Ksp", value: fmtE(ksp, 4),     unit:"", hi:1 },
      { label:"相对误差",   value: err.toFixed(2),   unit:"%" }
    ],
    badge: { cls: notes.length ? "warn" : "good",
             text: "实验温度 " + v.t + " K · χ(BaSO₄) = " + fmtE(d, 3) + " S/m" },
    rows: [
      { k:"λ₀(BaSO₄)",  v: fmtE(lam0, 4) + " S·m²/mol" },
      { k:"χ(BaSO₄)",   v: fmtE(d, 4) + " S/m" },
      { k:"溶解度 c",   v: fmtE(c, 4) + " mol/L" },
      { k:"溶度积 Ksp", v: fmtE(ksp, 4), cls:"hi" },
      { k:"相对误差",   v: err.toFixed(2) + " %" }
    ],
    chart: { kind:"bars", unit:"×10⁻¹⁰", bars:[
      { name:"测量值", value: ksp * 1e10 },
      { name:"理论值", value: REF.BaSO4_Ksp * 1e10 }
    ]},
    plain: [
      "表 3-3  电导法测定 BaSO4 溶度积",
      "去离子水电导率 = " + v.cw + " μS/cm",
      "饱和溶液电导率 = " + v.cs + " μS/cm",
      "实验温度 T = " + v.t + " K",
      "----------------------------------",
      "λ0(BaSO4) = " + fmtE(lam0, 4) + " S·m²/mol",
      "χ(BaSO4) = " + fmtE(d, 4) + " S/m",
      "溶解度 c = " + fmtE(c, 4) + " mol/L",
      "溶度积 Ksp = " + fmtE(ksp, 4),
      "相对误差 = " + err.toFixed(2) + " %"
    ]
  };
}
""",
})

EXPS.append({
    "file": "exp4-kinetics-ea",
    "tag": "表 3-4 / 3-5",
    "name": "反应速率·级数与活化能",
    "desc": "由 S₂O₈²⁻ 与 I⁻ 反应的褪色时间求反应级数与活化能",
    "fields": [
        {"key": "t1", "label": "试验 1 反应时间 t", "unit": "s", "def": 120},
        {"key": "t2", "label": "试验 2 反应时间 t", "unit": "s", "def": 240},
        {"key": "t3", "label": "试验 3 反应时间 t", "unit": "s", "def": 480},
        {"key": "t4", "label": "试验 4 反应时间 t", "unit": "s", "def": 300},
        {"key": "t5", "label": "试验 5 反应时间 t", "unit": "s", "def": 600},
        {"key": "T1",  "label": "第 1 组 温度 T", "unit": "K", "def": 288.15},
        {"key": "tt1", "label": "第 1 组 时间 t", "unit": "s", "def": 300},
        {"key": "T2",  "label": "第 2 组 温度 T", "unit": "K", "def": 298.15},
        {"key": "tt2", "label": "第 2 组 时间 t", "unit": "s", "def": 180},
        {"key": "T3",  "label": "第 3 组 温度 T", "unit": "K", "def": 308.15},
        {"key": "tt3", "label": "第 3 组 时间 t", "unit": "s", "def": 110},
    ],
    "compute": r"""
function (v) {
  var VT = 50.0, dS2O8 = 0.010*8/(2*VT);
  var VOLS = [[20,20],[10,20],[5,20],[20,10],[20,5]];
  var ts = [];
  for (var i=0;i<5;i++){
    var t = v["t" + (i+1)];
    if (!(t > 0)) return { err:"试验 " + (i+1) + " 的反应时间必须大于 0" };
    ts.push(t);
  }
  var vv = [];
  for (var k=0;k<5;k++) vv.push(dS2O8 / ts[k]);
  var m = Math.log(vv[0]/vv[2]) / Math.log(VOLS[0][0]/VOLS[2][0]);
  var n = Math.log(vv[0]/vv[4]) / Math.log(VOLS[0][1]/VOLS[4][1]);

  var rows = [
    { k:"反应级数 m (对 S₂O₈²⁻)", v: m.toFixed(2) },
    { k:"反应级数 n (对 I⁻)",      v: n.toFixed(2) },
    { k:"总级数 m + n",            v: (m+n).toFixed(2), cls:"hi" }
  ];
  var plain = ["表 3-4/3-5  反应速率·级数与活化能", "------------------------------",
               "反应级数 m = " + m.toFixed(2), "反应级数 n = " + n.toFixed(2),
               "总级数 m+n = " + (m+n).toFixed(2), "------------------------------"];

  var Ts = [v.T1, v.T2, v.T3];
  var seen = {}, dup = false;
  Ts.forEach(function(x){ if (seen[x]) dup = true; seen[x] = 1; });
  if (dup){
    rows.push({ k:"错误：三组温度必须互不相同", v:"", cls:"err" });
    return { rows: rows, notes: [], chart: null, plain: plain };
  }
  var cs4 = 0.2*20/VT, ci4 = 0.2*10/VT;
  var invTs = [], lgks = [];
  for (var g=0;g<3;g++){
    var tg = v["tt" + (g+1)];
    if (!(tg > 0)) return { err:"第 " + (g+1) + " 组的反应时间必须大于 0" };
    var kk = (dS2O8 / tg) / (Math.pow(cs4, m) * Math.pow(ci4, n));
    invTs.push(1/Ts[g]); lgks.push(Math.log10(kk));
    rows.push({ k:"T = " + Ts[g].toFixed(2) + " K", v:"k = " + fmtE(kk, 4) });
    plain.push("T = " + Ts[g].toFixed(2) + " K   k = " + fmtE(kk, 4));
  }
  var fit = linfit(invTs, lgks);
  if (!fit) return { err:"数据无法拟合，请检查三组温度与时间" };
  var slope = fit[0], intercept = fit[1];
  var Ea  = -slope * 2.303 * REF.R / 1000;
  var err = Math.abs(Ea - REF.Ea) / REF.Ea * 100;
  rows.push({ k:"活化能 Ea",            v: Ea.toFixed(2) + " kJ/mol", cls:"hi" });
  rows.push({ k:"相对误差 (文献值 51.8 kJ/mol)", v: err.toFixed(2) + " %" });
  plain.push("斜率 = " + fmtE(slope, 3));
  plain.push("活化能 Ea = " + Ea.toFixed(2) + " kJ/mol");
  plain.push("相对误差 = " + err.toFixed(2) + " %");

  var lo = Math.min.apply(null, invTs), hi = Math.max.apply(null, invTs);
  return {
    rows: rows, notes: [], plain: plain,
    kpis: [
      { label:"反应级数 m",   value: m.toFixed(2),     unit:"" },
      { label:"反应级数 n",   value: n.toFixed(2),     unit:"" },
      { label:"总级数 m + n", value: (m+n).toFixed(2), unit:"", hi:1 },
      { label:"活化能 Ea",    value: Ea.toFixed(2),    unit:"kJ/mol", hi:1 }
    ],
    badge: { cls:"good", text:"三组温度 " + Ts[0] + " / " + Ts[1] + " / " + Ts[2] + " K" },
    chart: { kind:"xy", xlabel:"1/T (K⁻¹)", ylabel:"lg k",
      points: invTs.map(function(x, i){ return [x, lgks[i]]; }),
      lines: [ { points: [[lo, slope*lo+intercept], [hi, slope*hi+intercept]], label:"线性拟合" } ],
      marks: [],
      legend: [ { label:"实验点" }, { label:"线性拟合" } ] }
  };
}
""",
})

EXPS.append({
    "file": "exp5-complex-k",
    "tag": "表 3-5",
    "name": "配合物组成与稳定常数",
    "desc": "等摩尔系列法测磺基水杨酸合铁(Ⅲ) 的组成与稳定常数 K稳",
    "fields": [
        {"key": "a1",  "label": "1 号溶液 吸光度 A",  "unit": "", "def": 0.10},
        {"key": "a2",  "label": "2 号溶液 吸光度 A",  "unit": "", "def": 0.19},
        {"key": "a3",  "label": "3 号溶液 吸光度 A",  "unit": "", "def": 0.28},
        {"key": "a4",  "label": "4 号溶液 吸光度 A",  "unit": "", "def": 0.37},
        {"key": "a5",  "label": "5 号溶液 吸光度 A",  "unit": "", "def": 0.46},
        {"key": "a6",  "label": "6 号溶液 吸光度 A",  "unit": "", "def": 0.55},
        {"key": "a7",  "label": "7 号溶液 吸光度 A",  "unit": "", "def": 0.50},
        {"key": "a8",  "label": "8 号溶液 吸光度 A",  "unit": "", "def": 0.42},
        {"key": "a9",  "label": "9 号溶液 吸光度 A",  "unit": "", "def": 0.33},
        {"key": "a10", "label": "10 号溶液 吸光度 A", "unit": "", "def": 0.22},
        {"key": "a11", "label": "11 号溶液 吸光度 A", "unit": "", "def": 0.11},
    ],
    "compute": r"""
function (v) {
  var VOLS = [[10,0],[9,1],[8,2],[7,3],[6,4],[5,5],[4,6],[3,7],[2,8],[1,9],[0,10]];
  var A = [], TL = [];
  for (var i=0;i<11;i++){
    var a = v["a" + (i+1)];
    if (!isFinite(a)) return { err:(i+1) + " 号溶液吸光度无效" };
    A.push(a);
    TL.push(VOLS[i][1] / (VOLS[i][0] + VOLS[i][1]));
  }
  var idx = 0;
  for (var j=1;j<11;j++) if (A[j] > A[idx]) idx = j;
  if (idx < 2 || idx > 8)
    return { err:"吸光度最大值出现在端点附近（两侧各不足 2 个点），无法做左右线性外推，请检查数据" };

  var tlMax = TL[idx], LX = [], LY = [], RX = [], RY = [];
  for (var p=0;p<11;p++){
    if (TL[p] < tlMax){ LX.push(TL[p]); LY.push(A[p]); }
    if (TL[p] > tlMax){ RX.push(TL[p]); RY.push(A[p]); }
  }
  var f1 = linfit(LX, LY), f2 = linfit(RX, RY);
  if (!f1 || !f2) return { err:"左右两侧数据不足以拟合，请检查吸光度" };
  if (f1[0] === f2[0]) return { err:"左右两侧拟合斜率相同，无法求交点，请检查数据" };

  var tlStar = (f2[1]-f1[1]) / (f1[0]-f2[0]);
  var A1 = f1[0]*tlStar + f1[1];
  var A2 = A[idx];
  if (!(tlStar > 0 && tlStar < 1) || !(A1 > 0))
    return { err:"两侧拟合交点不合理，请检查吸光度数据" };
  var alpha = (A1 - A2) / A1;
  if (!(alpha > 0)) return { err:"解离度 α ≤ 0，请检查数据" };

  var nb = tlStar / (1 - tlStar);
  var c  = 0.0010 * (10 * (1 - tlStar)) / 20;
  var K  = (1 - alpha) / (c * alpha * alpha);

  return {
    notes: [],
    kpis: [
      { label:"组成 n",       value: "1 : " + nb.toFixed(2), unit:"", hi:1 },
      { label:"解离度 α",     value: alpha.toFixed(4),       unit:"" },
      { label:"总浓度 c",     value: fmtE(c, 4),             unit:"mol/L" },
      { label:"稳定常数 K稳", value: fmtE(K, 3),             unit:"", hi:1 }
    ],
    badge: { cls:"good", text:"极大点落在 " + (idx+1) + " 号溶液 · TL = " + tlStar.toFixed(3) },
    rows: [
      { k:"理论极大 A₁",        v: A1.toFixed(4) + "  @ TL=" + tlStar.toFixed(3) },
      { k:"实验极大 A₂",        v: A2.toFixed(4) },
      { k:"组成 n (Fe:H₃R)",    v: "1 : " + nb.toFixed(2) },
      { k:"解离度 α",           v: alpha.toFixed(4) },
      { k:"总浓度 c",           v: fmtE(c, 4) + " mol/L" },
      { k:"稳定常数 K稳",       v: fmtE(K, 3), cls:"hi" }
    ],
    chart: { kind:"xy", xlabel:"配体摩尔分数 TL", ylabel:"吸光度 A",
      points: TL.map(function(x, i){ return [x, A[i]]; }),
      lines: [
        { points: [[0, f1[1]], [tlStar, A1]], label:"左拟合" },
        { points: [[tlStar, A1], [1, f2[0]+f2[1]]], label:"右拟合" }
      ],
      marks: [ { x: tlStar, y: A1 } ],
      legend: [ { label:"实验点" }, { label:"左拟合" }, { label:"右拟合" }, { label:"理论极大" } ] },
    plain: [
      "表 3-5  等摩尔系列法测配合物组成与稳定常数",
      "吸光度 A = " + A.join(", "),
      "----------------------------------",
      "理论极大 A1 = " + A1.toFixed(4) + "  @ TL = " + tlStar.toFixed(3),
      "实验极大 A2 = " + A2.toFixed(4),
      "组成 n = 1 : " + nb.toFixed(2),
      "解离度 α = " + alpha.toFixed(4),
      "总浓度 c = " + fmtE(c, 4) + " mol/L",
      "稳定常数 K稳 = " + fmtE(K, 3)
    ]
  };
}
""",
})


# ============================================================
# 理论与主要公式（两版共用，直接生成 HTML）
# ============================================================
THEORY = {
    "exp1-mg-molar-mass": {
        "items": [
            ("反应方程", "Mg + H<sub>2</sub>SO<sub>4</sub> → MgSO<sub>4</sub> + H<sub>2</sub>↑"),
            ("理想气体状态方程", "pV = nRT"),
            ("氢气分压", "p(H<sub>2</sub>) = p<sub>大气</sub> − p(H<sub>2</sub>O)"),
            ("摩尔质量", "M(Mg) = [ m·R·T ] / [ p(H<sub>2</sub>)·V ]"),
            ("相对误差", "δ = | M<sub>测</sub> − M<sub>理</sub> | / M<sub>理</sub> × 100%"),
        ],
        "note": "V 取 (V₂ − V₁) 并换算为 m³，m 换算为 kg，R = 8.314 J·mol⁻¹·K⁻¹；"
                "p(H₂) 必须用大气压扣掉该温度下水的饱和蒸气压。",
    },
    "exp2-acetic-ka": {
        "items": [
            ("电离平衡", "HAc ⇌ H<sup>+</sup> + Ac<sup>−</sup>"),
            ("电离常数定义", "K<sub>a</sub> = c(H<sup>+</sup>)·c(Ac<sup>−</sup>) / c(HAc)"),
            ("由 pH 求氢离子浓度", "c(H<sup>+</sup>) = 10<sup>−pH</sup>"),
            ("电离度", "α = c(H<sup>+</sup>) / c<sub>0</sub> × 100%"),
            ("α &lt; 5 % 时（式 3-8）", "K<sub>a</sub> = c(H<sup>+</sup>)<sup>2</sup> / c"),
            ("α ≥ 5 % 时（式 3-6）", "K<sub>a</sub> = c(H<sup>+</sup>)<sup>2</sup> / [ c − c(H<sup>+</sup>) ]"),
        ],
        "note": "α 很小时可忽略已电离部分，用式 3-8；α 较大时必须用式 3-6 扣除 c(H⁺)。"
                "4 份溶液的浓度由 c = c₀·V(HAc) / [V(HAc) + V(H₂O)] 算出。",
    },
    "exp3-baso4-ksp": {
        "items": [
            ("溶解平衡", "BaSO<sub>4</sub>(s) ⇌ Ba<sup>2+</sup> + SO<sub>4</sub><sup>2−</sup>"),
            ("扣除水的本底电导率", "χ(BaSO<sub>4</sub>) = χ(溶液) − χ(H<sub>2</sub>O)"),
            ("由电导率求浓度", "c = χ(BaSO<sub>4</sub>) / ( λ<sub>0</sub> × 1000 )"),
            ("溶度积", "K<sub>sp</sub> = c(Ba<sup>2+</sup>)·c(SO<sub>4</sub><sup>2−</sup>) = c<sup>2</sup>"),
        ],
        "note": "χ 以 μS/cm 输入，程序内部换算为 S/m 后代入；λ₀ 取该温度下的极限摩尔电导率，"
                "只有当 BaSO₄ 完全电离且溶液无限稀时才可用。",
    },
    "exp4-kinetics-ea": {
        "items": [
            ("速率方程", "v = k · c(S<sub>2</sub>O<sub>8</sub><sup>2−</sup>)<sup>m</sup> · c(I<sup>−</sup>)<sup>n</sup>"),
            ("以褪色时间度量速率", "v ∝ 1 / t"),
            ("反应级数 m", "m = lg( v<sub>1</sub> / v<sub>3</sub> ) / lg( c<sub>1</sub> / c<sub>3</sub> )"),
            ("反应级数 n", "n = lg( v<sub>1</sub> / v<sub>5</sub> ) / lg( c<sub>1</sub> / c<sub>5</sub> )"),
            ("阿伦尼乌斯方程", "lg k = lg A − E<sub>a</sub> / ( 2.303 R T )"),
            ("活化能", "E<sub>a</sub> = − 斜率 × 2.303 R"),
        ],
        "note": "反应消耗的 Δc(S₂O₈²⁻) = c(S₂O₃²⁻) / 2，各组保持一致；"
                "由 lg k 对 1/T 作直线，斜率 k = −Ea / (2.303 R)，据此求活化能。",
    },
    "exp5-complex-k": {
        "items": [
            ("配体摩尔分数", "TL = n(H<sub>3</sub>R) / [ n(Fe<sup>3+</sup>) + n(H<sub>3</sub>R) ]"),
            ("组成", "n = TL* / ( 1 − TL* )"),
            ("解离度", "α = ( A<sub>1</sub> − A<sub>2</sub> ) / A<sub>1</sub>"),
            ("稳定常数", "K<sub>稳</sub> = ( 1 − α ) / ( c · α<sup>2</sup> )"),
        ],
        "note": "等摩尔系列法：以吸光度 A 对配体摩尔分数 TL 作图，两侧直线段的交点 TL* "
                "即配合物组成点；A₁ 为交点处的理论极大吸光度，A₂ 为实测极大吸光度。",
    },
}


def theory_html(t):
    parts = ['<div class="theory-grid">']
    for label, expr in t["items"]:
        parts.append('<div class="fm"><span class="fl">%s</span>'
                     '<span class="fx">%s</span></div>' % (label, expr))
    parts.append("</div>")
    if t.get("note"):
        parts.append('<p class="theory-note">%s</p>' % t["note"])
    return "".join(parts)


for _e in EXPS:
    _e["theory"] = theory_html(THEORY[_e["file"]])


# ============================================================
# 页面模板
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
<div class="bg"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span><span class="blob b4"></span></div>
<main class="wrap">
  <nav class="tabs" id="tabs"></nav>
  <header class="card head">
    <div>
      <h1 id="expName"></h1>
      <p class="sub" id="expDesc"></p>
    </div>
    <span class="tag" id="expTag"></span>
  </header>
  <div class="cols">
    <section class="card">
      <h2>数据输入</h2>
      <div id="fields"></div>
      <div class="row">
        <button class="btn primary" id="btnCalc">计 算</button>
        <button class="btn" id="btnReset">重 置</button>
      </div>
      <div id="msg"></div>
    </section>
    <section class="card">
      <h2>计算结果</h2>
      <div class="res" id="results" aria-live="polite"></div>
      <div class="chart-box"><canvas id="chart"></canvas></div>
      <div class="export">
        <div class="hint">把结果填进实验报告：</div>
        <div class="row" style="margin-top:0">
          <button class="btn sm" id="btnCopy">复制结果</button>
          <button class="btn sm" id="btnCsv">下载 CSV</button>
          <button class="btn sm" id="btnText">显示纯文本</button>
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
<footer id="footer"></footer>
<script>
"use strict";
/* ===== 实验定义（必须在运行时之前） ===== */
var EXPS = [@@DATA@@];
@@RUNTIME@@
</script>
</body>
</html>
"""


def render_page(exps, title):
    data = ",\n".join(
        "{\n  tag: %s,\n  name: %s,\n  desc: %s,\n  fields: %s,\n  theory: %s,\n  compute: %s\n}"
        % (js_str(e["tag"]), js_str(e["name"]), js_str(e["desc"]),
           js_fields(e["fields"]), js_str(e["theory"]), e["compute"])
        for e in exps
    )
    return (PAGE
            .replace("@@TITLE@@", title)
            .replace("@@CSS@@", CSS)
            .replace("@@RUNTIME@@", RUNTIME)
            .replace("@@DATA@@", data))


def js_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def js_fields(fields):
    items = []
    for f in fields:
        items.append('{ key:%s, label:%s, unit:%s, def:%s }'
                     % (js_str(f["key"]), js_str(f["label"]),
                        js_str(f["unit"]), repr(f["def"])))
    return "[" + ", ".join(items) + "]"


# ============================================================
# 目录页
# ============================================================
WARN_JS = r"""<script>
(function(){
  function warn(force){
    if (!force && location.protocol !== "file:") return;
    var p = decodeURIComponent(location.pathname);
    if (!force && !/Temp/i.test(p)) return;
    if (document.getElementById("zip-warn")) return;
    var d = document.createElement("div");
    d.id = "zip-warn";
    d.innerHTML =
      "<b>&#9888; 检测到可能是直接从压缩包里打开的</b><br>" +
      "从压缩包里双击，系统只会解出这一个文件，所以点下面的链接会报「找不到文件」。<br>" +
      "正确做法：<b>右键压缩包 &rarr; 全部解压</b>，进入解压出来的文件夹后，再双击 " +
      "<b>index.html</b>。<br>" +
      "另外：<b>all-in-one.html</b> 是单文件版，随便怎么打开都能用。";
    d.style.cssText =
      "position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#fff7ed;" +
      "color:#9a3412;border-top:2px solid #fdba74;padding:14px 20px;" +
      "font-size:13px;line-height:1.85;box-shadow:0 -6px 20px rgba(0,0,0,.12)";
    document.body.appendChild(d);
  }
  window.__warnIfFromArchive = warn;
  warn(false);
})();
</script>
"""

INDEX = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>化学实验数据处理系统 · 目录</title>
<style>
@@CSS@@
  .list{display:grid;grid-template-columns:1fr;gap:12px}
  @media (min-width:700px){.list{grid-template-columns:1fr 1fr}}
  .item{display:flex;flex-direction:column;gap:6px;padding:16px 18px;border-radius:14px;
        text-decoration:none;color:inherit;
        background:rgba(255,255,255,.62);border:1px solid rgba(255,255,255,.92);
        transition:all .16s}
  .item:hover{background:#fff;transform:translateY(-2px);
              box-shadow:0 12px 28px rgba(15,23,42,.12)}
  .item .t{font-size:11px;font-weight:700;color:var(--acc2)}
  .item .n{font-size:15px;font-weight:700}
  .item .d{font-size:11.5px;color:var(--dim);line-height:1.5}
</style>
</head>
<body>
<div class="bg"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span><span class="blob b4"></span></div>
<main class="wrap">
  <header class="card head">
    <div>
      <h1>化学实验数据处理系统 · 网页版</h1>
      <p class="sub">共 5 个实验。每个实验一个独立页面，可直接打开，也可用 iframe 嵌入课程平台。</p>
    </div>
    <span class="tag">v1.0</span>
  </header>
  <section class="card">
    <h2>实验列表</h2>
    <div class="list">@@ITEMS@@</div>
  </section>
  <section class="card">
    <h2>另有：单文件合并版</h2>
    <p class="sub" style="margin-top:0">
      如果不想放 5 个文件，可以用合并版 —— 一个 HTML 里用标签页切换全部 5 个实验。<br>
      <a href="all-in-one.html" style="color:var(--acc);font-weight:700">打开 all-in-one.html →</a>
    </p>
  </section>
</main>
<footer>化学实验常数测定数据处理 · 网页版 v2.0</footer>
@@WARN@@
</body>
</html>
"""


# ============================================================
# 说明文档
# ============================================================
README_TXT = """化学实验数据处理系统（网页版）v1.0
================================================

一、这个包里有什么
------------------------------------------------
  index.html                入口目录页（列出 5 个实验）
  exp1-mg-molar-mass.html       表 3-1  量气法测定镁的摩尔质量
  exp2-acetic-ka.html           表 3-2  pH 法测乙酸电离常数
  exp3-baso4-ksp.html           表 3-3  电导法测 BaSO4 溶度积
  exp4-kinetics-ea.html         表 3-4/3-5  反应速率·级数与活化能
  exp5-complex-k.html           表 3-5  配合物组成与稳定常数
  all-in-one.html           单文件合并版（标签页切换 5 个实验）
  嵌入代码.txt              每页对应的 iframe 代码，可直接复制
  本地预览.bat              双击启动本地预览（需已安装 Python）

二、技术特点（重要）
------------------------------------------------
  1. 全部为零依赖的单文件网页：CSS / JavaScript 全部内联，
     不引用任何 CDN、不需要安装任何库、不需要服务器端程序。
  2. 计算全部在浏览器本地完成，不上传任何数据。
  3. 所有文件都可以直接用浏览器双击打开，也可以放到任意
     静态服务器上。

三、两种部署方式
------------------------------------------------
【方式 A】上传网页文件（如果能用）
  直接把 html 文件作为课程资源上传。
  注意：部分平台的 HTML 安全过滤会删除页面里的 <script> 标签，
        一旦被删，页面就无法计算。上传后请务必点一下页面上
        的「计算」按钮验证。

【方式 B】iframe 嵌入外链（推荐）
  1. 把这几个 html 放到一个可以通过 https 访问的静态空间，
     例如：学校服务器 / GitHub Pages / 对象存储（OSS、COS）/ 超星云盘。
  2. 在课程章节编辑里选择「插入 iframe / 网页」，粘贴
     「嵌入代码.txt」里对应的那一段即可。

四、iframe 嵌入注意事项
------------------------------------------------
  1. 地址必须是 https（http 地址多数课程平台会拦截）。
  2. 服务器不要设置 X-Frame-Options: DENY。
  3. 建议高度 700；页面已做自适应，宽度写 100% 即可。
  4. 在网址后面加上 ?embed=1 会进入"嵌入模式"：
     隐藏页脚、收紧留白、自动变双栏，一屏能放下。
  5. 网址结尾拼 &from=chaoxing 之类的参数不影响使用。

五、学生怎么用 / 怎么交作业
------------------------------------------------
  1. 在「数据输入」里填入实验测得的数据。
  2. 点「计算」，右侧出现结果和图表。
  3. 点「复制结果」——结果文本进剪贴板，可直接粘到实验报告。
     点「下载 CSV」——导出 Excel 可打开的表格文件。
     （注意：file:// 直接打开时浏览器不给剪贴板权限，此时请用
       「显示纯文本」按钮，把文本手动复制走。）

六、浏览器要求
------------------------------------------------
  Chrome / Edge 76+ ，Firefox 103+ ，Safari 9+ 。
  老浏览器上毛玻璃效果会自动降级为半透明色块，功能不受影响。

七、本地预览
------------------------------------------------
  双击「本地预览.bat」，然后在浏览器打开：
      http://localhost:8765/index.html
  （需要电脑上已安装 Python；不需要安装任何第三方包）

================================================
"""


def embed_snippets(base_url):
    lines = ["iframe 嵌入代码（把 base 换成你实际的网址）", "=" * 60, ""]
    for e in EXPS:
        lines.append("【%s  %s】" % (e["tag"], e["name"]))
        lines.append(
            '<iframe src="%s/%s.html?embed=1" width="100%%" height="700"\n'
            '        style="border:none;border-radius:12px" loading="lazy"\n'
            '        title="%s"></iframe>' % (base_url, e["file"], e["name"]))
        lines.append("")
    lines.append("【单文件合并版（5 个实验合一）】")
    lines.append(
        '<iframe src="%s/all-in-one.html?embed=1" width="100%%" height="800"\n'
        '        style="border:none;border-radius:12px" loading="lazy"\n'
        '        title="化学实验数据处理"></iframe>' % base_url)
    return "\n".join(lines)


PREVIEW_BAT = """@echo off
cd /d "%~dp0"
echo.
echo   化学实验数据处理系统 - 本地预览
echo   启动后请在浏览器打开:  http://localhost:8765/index.html
echo   关闭本窗口即停止服务。
echo.
python -m http.server 8765
pause
"""


# ============================================================
# 主流程
# ============================================================
def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    for e in EXPS:
        html = render_page([e], e["name"] + " · 化学实验数据处理")
        with open(os.path.join(OUT, e["file"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        log("  生成 " + e["file"] + ".html")

    html = render_page(EXPS, "化学实验数据处理系统 · 5 个实验")
    with open(os.path.join(OUT, "all-in-one.html"), "w", encoding="utf-8") as f:
        f.write(html)
    log("  生成 all-in-one.html")

    items = []
    for e in EXPS:
        items.append(
            '<a class="item" href="%s.html">\n'
            '  <span class="t">%s</span>\n'
            '  <span class="n">%s</span>\n'
            '  <span class="d">%s</span>\n'
            '</a>' % (e["file"], e["tag"], e["name"], e["desc"]))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.replace("@@CSS@@", CSS)
                     .replace("@@ITEMS@@", "\n".join(items))
                     .replace("@@WARN@@", WARN_JS))
    log("  生成 index.html")
    log("完成（说明文档与打包见 package.py）。")


if __name__ == "__main__":
    main()
