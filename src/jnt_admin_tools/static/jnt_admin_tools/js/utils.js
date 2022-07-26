var loadScripts = function (js_files, onComplete) {
  const len = js_files.length;
  const head = document.getElementsByTagName('head')[0];

  function loadScript(index) {
    let testOk;

    if (index >= len) {
      onComplete();
      return;
    }

    try {
      testOk = js_files[index].test();
    } catch (e) {
      // with certain browsers like opera the above test can fail
      // because of undefined variables...
      testOk = true;
    }

    if (testOk) {
      const s = document.createElement('script');
      s.src = js_files[index].src;
      s.type = 'text/javascript';
      head.appendChild(s);
      if (/MSIE/.test(navigator.userAgent)) {
        // Internet Explorer
        s.onreadystatechange = function () {
          if (s.readyState === 'loaded' || s.readyState === 'complete') {
            loadScript(index + 1);
          }
        };
      } else {
        s.onload = function () {
          loadScript(index + 1);
        };
      }
    } else {
      loadScript(index + 1);
    }
  }

  loadScript(0);
}
