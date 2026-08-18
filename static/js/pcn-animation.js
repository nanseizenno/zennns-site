
(() => {
  "use strict";

  const STEPS = [
    {name:"signals", duration:1725, status:"多源设备 / 系统信号进入 PCN"},
    {name:"cae", duration:2025, status:"PCN 将信号映射到 C / A / E"},
    {name:"matrix", duration:2250, status:"CAE × SDB 形成 9 个判定坐标"},
    {name:"scan", duration:2550, status:"对 9 个判定坐标进行检查"},
    {name:"hit", duration:2250, status:"本次判定触发 E-D：Downstream state not refreshed"},
    {name:"wait", duration:2250, status:"Active result set {E-D} → Arbitration → Wait / Refresh"},
    {name:"refresh", duration:2325, status:"状态刷新后重新进入 PCN 判定"},
    {name:"allow", duration:2850, status:"判定恢复正常 → Normal Execution Chain → Target State"}
  ];

  const q=(r,s)=>r.querySelector(s);
  const qa=(r,s)=>[...r.querySelectorAll(s)];
  const on=(r,s)=>qa(r,s).forEach(e=>e.classList.add("is-on"));
  const flow=(r,s,k="is-flow")=>qa(r,s).forEach(e=>{e.classList.add("is-on",k)});

  function reset(root){
    root.classList.remove("is-allow","is-paused");
    qa(root,".is-on,.is-flow,.is-warnline,.is-okline,.is-active,.is-scan,.is-hit,.is-selected")
      .forEach(e=>e.classList.remove("is-on","is-flow","is-warnline","is-okline","is-active","is-scan","is-hit","is-selected"));

    const note=q(root,"[data-matrix-note]");
    const rc=q(root,"[data-result-code]");
    const rd=q(root,"[data-result-desc]");
    const ac=q(root,"[data-arb-choice]");
    const tv=q(root,"[data-target-value]");
    const tt=q(root,"[data-trace-text]");
    if(note)note.textContent="Active result set: none";
    if(rc)rc.textContent="E-D";
    if(rd)rd.textContent="Downstream state not refreshed";
    if(ac)ac.textContent="Wait / Refresh";
    if(tv)tv.textContent="Not Entered";
    if(tt)tt.textContent="1st: E-D → Wait / Refresh";
  }

  function baseSignals(root){
    qa(root,"[data-src]").forEach(e=>e.classList.add("is-active"));
    flow(root,'[data-line^="sig"]');
  }

  function showCAE(root){
    on(root,'[data-part="cae"]');
    qa(root,"[data-domain]").forEach(e=>e.classList.add("is-active"));
  }

  function showMatrix(root){
    on(root,'[data-part="matrix"]');
  }

  function render(root, step){
    reset(root);
    baseSignals(root);

    if(["cae","matrix","scan","hit","wait","refresh","allow"].includes(step)){
      showCAE(root);
    }
    if(["matrix","scan","hit","wait","refresh","allow"].includes(step)){
      showMatrix(root);
    }

    if(step==="scan"){
      qa(root,"[data-cell]").forEach((cell,i)=>{
        setTimeout(()=>cell.classList.add("is-scan"), i*85);
      });
    }

    if(["hit","wait","refresh"].includes(step)){
      q(root,'[data-cell="E-D"]')?.classList.add("is-hit");
      const note=q(root,"[data-matrix-note]");
      if(note)note.textContent="Active result set: {E-D}";
      on(root,'[data-part="result"]');
      q(root,'[data-part="result"]')?.classList.add("is-hit");
      flow(root,'[data-line="matrix_to_result"]',"is-warnline");
    }

    if(["wait","refresh"].includes(step)){
      on(root,'[data-part="arb"]');
      q(root,'[data-part="arb"]')?.classList.add("is-hit");
      flow(root,'[data-line="result_to_arb"]',"is-warnline");
      on(root,'[data-path]');
      q(root,'[data-path="wait"]')?.classList.add("is-selected");
      flow(root,'[data-line="arb_to_wait"]',"is-warnline");
      flow(root,'[data-line="arb_to_recheck"],[data-line="arb_to_manual"],[data-line="arb_to_prohibit"],[data-line="arb_to_normal"]');
      on(root,'[data-part="trace"]');
    }

    if(step==="refresh"){
      on(root,'[data-part="refresh"]');
      const tt=q(root,"[data-trace-text]");
      if(tt)tt.textContent="1st: E-D → Wait / Refresh  |  Re-evaluating…";
    }

    if(step==="allow"){
      root.classList.add("is-allow");
      const note=q(root,"[data-matrix-note]");
      const rc=q(root,"[data-result-code]");
      const rd=q(root,"[data-result-desc]");
      const ac=q(root,"[data-arb-choice]");
      const tv=q(root,"[data-target-value]");
      const tt=q(root,"[data-trace-text]");
      if(note)note.textContent="Active result set: none";
      if(rc)rc.textContent="OK";
      if(rd)rd.textContent="No blocking coordinate";
      if(ac)ac.textContent="Normal Execution";
      if(tv)tv.textContent="Entered / Executing";
      if(tt)tt.textContent="1st: E-D → Wait  |  2nd: Normal → Target State";

      on(root,'[data-part="result"],[data-part="arb"],[data-path],[data-part="target"],[data-part="trace"]');
      flow(root,'[data-line="matrix_to_result"],[data-line="result_to_arb"],[data-line="arb_to_normal"],[data-line="normal_to_target"]',"is-okline");
    }
  }

  function init(root){
    const status=q(root,"[data-pcn3-status]");
    const autoBtn=q(root,"[data-pcn3-auto]");
    const manualBtn=q(root,"[data-pcn3-manual]");
    const prevBtn=q(root,"[data-pcn3-prev]");
    const nextBtn=q(root,"[data-pcn3-next]");
    const counter=q(root,"[data-pcn3-counter]");
    const reduced=window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;

    let idx=0;
    let timer=null;
    let mode=reduced ? "manual" : "auto";
    let hoverPaused=false;

    function updateControls(){
      const auto = mode==="auto";
      autoBtn?.classList.toggle("is-selected", auto);
      manualBtn?.classList.toggle("is-selected", !auto);
      autoBtn?.setAttribute("aria-pressed", auto ? "true" : "false");
      manualBtn?.setAttribute("aria-pressed", auto ? "false" : "true");
      if(counter) counter.textContent=`${idx+1} / ${STEPS.length}`;
    }

    function apply(){
      const s=STEPS[idx];
      render(root,s.name);
      if(status)status.textContent=s.status;
      updateControls();
    }

    function stopTimer(){
      clearTimeout(timer);
      timer=null;
    }

    function schedule(){
      stopTimer();
      if(mode!=="auto" || hoverPaused || reduced) return;
      timer=setTimeout(()=>{
        idx=(idx+1)%STEPS.length;
        apply();
        schedule();
      },STEPS[idx].duration);
    }

    function setMode(nextMode){
      mode=nextMode;
      stopTimer();
      root.classList.toggle("is-paused", mode==="manual" || hoverPaused);
      updateControls();
      if(mode==="auto") schedule();
    }

    function go(delta){
      setMode("manual");
      idx=(idx+delta+STEPS.length)%STEPS.length;
      apply();
    }

    autoBtn?.addEventListener("click",()=>setMode("auto"));
    manualBtn?.addEventListener("click",()=>setMode("manual"));
    prevBtn?.addEventListener("click",()=>go(-1));
    nextBtn?.addEventListener("click",()=>go(1));

    root.addEventListener("mouseenter",()=>{
      if(mode==="auto"){
        hoverPaused=true;
        stopTimer();
        root.classList.add("is-paused");
      }
    });

    root.addEventListener("mouseleave",()=>{
      if(mode==="auto"){
        hoverPaused=false;
        root.classList.remove("is-paused");
        schedule();
      }
    });

    root.addEventListener("focusin",()=>{
      if(mode==="auto"){
        hoverPaused=true;
        stopTimer();
        root.classList.add("is-paused");
      }
    });

    root.addEventListener("focusout",e=>{
      if(mode==="auto" && !root.contains(e.relatedTarget)){
        hoverPaused=false;
        root.classList.remove("is-paused");
        schedule();
      }
    });

    if(reduced){
      idx=STEPS.length-1;
      mode="manual";
      apply();
      if(status)status.textContent="静态预览：Normal Execution Chain → Target State";
      return;
    }

    apply();
    schedule();
  }

  document.addEventListener("DOMContentLoaded",()=>document.querySelectorAll("[data-pcn3]").forEach(init));

})();
