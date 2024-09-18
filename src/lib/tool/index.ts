function __canvasWM({
    content = '',
    content_hash = '',
}: { content?: string; content_hash?: string } = {}): void {
    const args = arguments[0];
    const canvas = document.createElement('canvas');
    canvas.setAttribute('width', '180px');
    canvas.setAttribute('height', '240px');
    const ctx = canvas.getContext("2d");
    if (!ctx) return; // 确保获取到上下文

    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "16px Microsoft Yahei";
    ctx.fillStyle = "rgba(185, 185, 185, 1)";
    ctx.rotate(Math.PI / 180 * 30);
    ctx.fillText(content, 150, 50);
    ctx.fillText(content_hash, 155, 80);

    const base64Url = canvas.toDataURL();
    const __wm = document.querySelector('.__wm') as HTMLDivElement || document.createElement("div");
    const styleStr = `position:fixed;top:0;left:0;bottom: 0;width:100%;height:100%;z-index:999999;pointer-events:none;background-repeat:repeat;background-image:url('${base64Url}');opacity:0.18;`;
    __wm.setAttribute('style', styleStr);
    __wm.classList.add('__wm');

    if (!document.querySelector('.__wm')) {
        document.body.insertBefore(__wm, document.body.lastChild);
    }

    const MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
    if (MutationObserver) {
        let mo = new MutationObserver(function () {
            const __wm = document.querySelector('.__wm') as HTMLDivElement;
            if ((__wm && __wm.getAttribute('style') !== styleStr) || !__wm) {
                mo.disconnect();
                mo = null;
                __canvasWM(JSON.parse(JSON.stringify(args)));
            }
        });

        mo.observe(document.body, {
            attributes: true,
            subtree: true,
            childList: true,
        });
    }
}

// 导出 __canvasWM 函数
export { __canvasWM };
