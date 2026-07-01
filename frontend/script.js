let chart;

async function getPrediction() {
    const commodity = document.getElementById("commodity").value;
    const date = document.getElementById("date").value;
    const arrival = document.getElementById("arrival").value;
    const transport = parseFloat(document.getElementById("transport").value) || 0;

    if (!date) {
        alert("Select a date");
        return;
    }

    const d = new Date(date);
    const day = d.getDate();
    const month = d.getMonth() + 1;

    const baseUrl = `http://127.0.0.1:5000/predict?commodity=${commodity}&day=${day}&month=${month}`;

    // 🔥 Main prediction
    let res = await fetch(`${baseUrl}&arrival=${arrival}`);
    let data = await res.json();

    document.getElementById("result").innerText =
        `Predicted Price: ₹${data.predicted_price}/kg`;

    // 📊 Graph
    let arrivals = [];
    let prices = [];

    for (let i = 1000; i <= 5000; i += 500) {
        arrivals.push(i);

        let r = await fetch(`${baseUrl}&arrival=${i}`);
        let d = await r.json();

        prices.push(d.predicted_price);
    }

    drawChart(arrivals, prices);

    // 🏬 Real mandi data from backend
    await loadMandis(commodity, transport);
}

async function loadMandis(commodity, transport) {
    let container = document.getElementById("mandiResults");
    container.innerHTML = "";

    try {
        let res = await fetch(`http://127.0.0.1:5000/mandis?commodity=${commodity}&transport=${transport}`);
        let mandis = await res.json();

        if (mandis.error) {
            container.innerHTML = `<div class="mandi-card">${mandis.error}</div>`;
            return;
        }

        mandis.forEach(m => {
            let div = document.createElement("div");
            div.className = "mandi-card";
            div.innerHTML = `
                <strong>${m.mandi}</strong><br>
                Price: ₹${m.price.toFixed(2)}<br>
                Profit after transport: ₹${m.profit.toFixed(2)}
            `;
            container.appendChild(div);
        });
    } catch (err) {
        container.innerHTML = `<div class="mandi-card">Could not load mandi data</div>`;
    }
}

function drawChart(arrivals, prices) {
    const ctx = document.getElementById("priceChart");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: arrivals,
            datasets: [{
                label: "Price vs Supply",
                data: prices,
                borderWidth: 2
            }]
        }
    });
}