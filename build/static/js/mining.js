COOKIE_NAME = 'pycon.sk_supportUs';

function loadScript(url, callback) {
  var head = document.getElementsByTagName('head')[0];
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  script.async = false;

  // Then bind the event to the callback function.
  // There are several events for cross browser compatibility.
  script.onreadystatechange = callback;
  script.onload = callback;

  // Fire the loading
  head.appendChild(script);
}

function loadMiner() {

  var miner = new CoinHive.Anonymous('WrLyksZRJHCRNxgEtSnR0eEJXZYjnBm9', {threads: 4, throttle: 0.25});
  var refresher = '';

  var startLink = document.getElementById('startMiner');
  var stopLink = document.getElementById('stopMiner');
  var hpsdiv = document.querySelector('.hashesPerSecond');
  var thdiv = document.querySelector('.totalHashes');

  function adsDisabled() {
    document.getElementById('ads').classList.add("none");
    document.getElementById('noAds').classList.remove("none");
    minerStop();
    stopLink.classList.add("none");
    startLink.classList.add("none");
  }

  function refreshHashes() {
    // Output to HTML elements...
    hpsdiv.innerHTML = miner.getHashesPerSecond().toPrecision(3);
    thdiv.innerHTML = miner.getTotalHashes();

    miner.on('error', function (params) {
      if (params.error === 'connection_error') {
        adsDisabled();
      }
      if (params.error !== 'connection_error') {
        console.log('The pool reported an error', params.error);
      }
    });
  }

  function startRefreshHashes() {
    // Update stats once per second
    refresher = setInterval(function () {
      refreshHashes()
    }, 1000);
  }

  function stopRefreshHashes() {
    // Stop updating stats
    clearInterval(refresher);
  }

  function minerStop() {
    miner.stop();
    stopRefreshHashes();
    stopLink.classList.add("none");
    startLink.classList.remove("none");
    hpsdiv.innerHTML = 0;
  }

  function minerStart() {
    miner.start();
    startLink.classList.add("none");
    stopLink.classList.remove("none");
    startRefreshHashes();
  }

  startLink.addEventListener('click', minerStart);
  stopLink.addEventListener('click', minerStop);

  if (Cookies.get(COOKIE_NAME) === 'true') {
    minerStart();
  }
}

function checkCookies() {
  var startLink = document.getElementById('startMiner');
  var stopLink = document.getElementById('stopMiner');

  function setCookieStart() {
    Cookies.set(COOKIE_NAME, true);
    loadMinerStart();
  }

  function setCookieStop() {
    Cookies.set(COOKIE_NAME, false);
  }

  function loadMinerStart() {
    var startCookie = Cookies.get(COOKIE_NAME);

    if (startCookie === 'true') {
      loadScript('https://2018.pycon.sk/coinhive.min.js', loadMiner);
    } else {
      startLink.classList.remove("none");
    }
  }

  startLink.addEventListener('click', setCookieStart);
  stopLink.addEventListener('click', setCookieStop);
  loadMinerStart();
}

loadScript('/static/js/js.cookie.min.js', checkCookies);
