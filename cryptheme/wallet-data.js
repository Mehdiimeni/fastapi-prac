
    // Global wallet data
    let walletData = {};

    // Minimum withdrawal amounts
    const minWithdrawals = {
        BTC: 0.0000086,
        ETH: 0.0001,
        USDT: 10
    };

    // Unified loadWalletData function
    async function loadWalletData() {
        try {
            const response = await fetch('wallet-data.json');
            if (!response.ok) throw new Error('Failed to load wallet data');
            walletData = await response.json();
        } catch (error) {
            console.error('Error loading wallet data:', error);
            // Default data structure
            walletData = {
                spot: {
                    BTC: 0,
                    ETH: 0,
                    USDT: 0,
                    balance: 0,
                    buy: 0,
                    sell: 0,
                    value: 0
                },
                p2p: {
                    balance: 0,
                    buy: 0,
                    sell: 0,
                    value: 0
                },
                margin: {
                    balance: 0,
                    debt: 0,
                    equity: 0,
                    profit: { btc: 0, percent: 0, usd: 0, usdPercent: 0 }
                },
                future: {
                    balance: 0,
                    wallet: 0,
                    pnl: 0
                },
                earn: {
                    balance: 0,
                    locked: 0,
                    flexible: 0
                },
                transactions: []
            };
        }

        updateUI();
        updateWalletUI(walletData);
    }

    // Update withdrawal UI
    function updateUI() {
        const selectedCoin = document.getElementById('selected-coin')?.textContent || 'BTC';
        document.getElementById('current-balance').textContent = 
            `${walletData.spot[selectedCoin] || 0} ${selectedCoin}`;
        document.getElementById('min-withdrawal').textContent = 
            `${minWithdrawals[selectedCoin]} ${selectedCoin}`;
    }

    // Update full wallet UI (tabs)
    function updateWalletUI(data) {
        // Spot Tab
        document.getElementById('spot-balance').textContent = (data.spot?.balance || 0) + ' BTC';
        document.getElementById('spot-buy').textContent = (data.spot?.buy || 0) + ' BTC';
        document.getElementById('spot-sell').textContent = (data.spot?.sell || 0) + ' BTC';
        document.getElementById('spot-value').textContent = '$' + (data.spot?.value || 0).toLocaleString();

        // P2P Tab
        document.getElementById('p2p-balance').textContent = (data.p2p?.balance || 0) + ' BTC';
        document.getElementById('p2p-buy').textContent = (data.p2p?.buy || 0) + ' BTC';
        document.getElementById('p2p-sell').textContent = (data.p2p?.sell || 0) + ' BTC';
        document.getElementById('p2p-value').textContent = '$' + (data.p2p?.value || 0).toLocaleString();

        // Margin Tab
        const marginBalance = data.margin?.balance || 0;
        document.getElementById('margin-balance').textContent = `${marginBalance} BTC≈$${(marginBalance * 50000).toLocaleString()}`;
        document.getElementById('margin-debt').textContent = (data.margin?.debt || 0) + ' BTC';
        document.getElementById('margin-equity').textContent = (data.margin?.equity || 0) + ' BTC';
        const profit = data.margin?.profit || { btc: 0, percent: 0, usd: 0, usdPercent: 0 };
        document.getElementById('margin-profit').textContent = 
            `${profit.btc} BTC(${profit.percent}%) $${profit.usd} (${profit.usdPercent}%)`;

        // Future Tab
        const futureBalance = data.future?.balance || 0;
        document.getElementById('future-balance').textContent = `${futureBalance} BTC≈$${(futureBalance * 50000).toLocaleString()}`;
        document.getElementById('future-wallet').textContent = (data.future?.wallet || 0) + ' BTC';
        document.getElementById('future-pnl').textContent = (data.future?.pnl || 0) + ' BTC';

        // Earn Tab
        const earnBalance = data.earn?.balance || 0;
        document.getElementById('earn-balance').textContent = `${earnBalance} BTC≈$${(earnBalance * 50000).toLocaleString()}`;
        document.getElementById('earn-locked').textContent = (data.earn?.locked || 0) + ' BTC';
        document.getElementById('earn-flexible').textContent = (data.earn?.flexible || 0) + ' BTC';
    }

    // Save wallet data to server
    async function saveWalletData() {
        try {
            const response = await fetch('save-wallet.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(walletData)
            });
            if (!response.ok) throw new Error('Failed to save wallet data');
        } catch (error) {
            console.error('Error saving wallet data:', error);
        }
    }

    // Handle withdrawal form
    document.getElementById('withdraw-form')?.addEventListener('submit', async function(e) {
        e.preventDefault();

        const selectedCoin = document.getElementById('selected-coin').textContent;
        const amount = parseFloat(document.getElementById('withdraw-amount').value);
        const address = document.getElementById('withdraw-address').value;
        const network = document.getElementById('withdraw-network').value;

        if (!amount || amount <= 0) {
            alert('Please enter a valid amount');
            return;
        }

        if (!address) {
            alert('Please enter a withdrawal address');
            return;
        }

        if (amount < minWithdrawals[selectedCoin]) {
            alert(`Minimum withdrawal amount is ${minWithdrawals[selectedCoin]} ${selectedCoin}`);
            return;
        }

        if (!walletData.spot[selectedCoin] || walletData.spot[selectedCoin] < amount) {
            alert('Insufficient balance');
            return;
        }

        // Process withdrawal
        walletData.spot[selectedCoin] -= amount;

        walletData.transactions.push({
            date: new Date().toISOString(),
            type: 'withdrawal',
            coin: selectedCoin,
            amount: amount,
            address: address,
            network: network,
            status: 'completed'
        });

        updateUI();
        await saveWalletData();

        document.getElementById('withdraw-amount').value = '';
        document.getElementById('withdraw-address').value = '';
        alert(`Successfully withdrew ${amount} ${selectedCoin} to ${address}`);
    });

    // Handle coin dropdown
    document.querySelectorAll('#coin-dropdown .dropdown-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const coin = this.getAttribute('data-coin');
            document.getElementById('selected-coin').textContent = coin;
            document.getElementById('balance-label').textContent = `${coin} spot balance`;
            updateUI();
        });
    });

    // Init on page load
    document.addEventListener('DOMContentLoaded', loadWalletData);

