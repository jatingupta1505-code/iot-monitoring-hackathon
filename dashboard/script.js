const API_URL =
    "https://49i2l2svj8.execute-api.ap-south-1.amazonaws.com/default/FactoryDashboardAPI";


async function loadDashboard() {

    try {

        const response = await fetch(API_URL + "?t=" + Date.now());

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        console.log("Latest AWS Data:", data);

        updateDashboard(data);

    } catch (error) {

        console.error("Dashboard Error:", error);

    }
}


function updateDashboard(data) {

    const telemetry = data.latest_telemetry || {};
    const machine = data.machine || {};
    const alerts = data.alerts || [];


    // -------------------------
    // MACHINE STATUS
    // -------------------------

    const machineStatus = document.querySelector(".badge");

    if (machineStatus) {

        if (machine.status === "Online") {

            machineStatus.textContent = "● ONLINE";
            machineStatus.className = "badge online";

        } else {

            machineStatus.textContent = "● OFFLINE";
            machineStatus.className = "badge offline";

        }

    }


    // -------------------------
    // TEMPERATURE & PRESSURE
    // -------------------------

    const metrics = document.querySelectorAll(".metric strong");

    if (metrics.length >= 2) {

        metrics[0].textContent =
            `${telemetry.temperature ?? "--"}°C`;

        metrics[1].textContent =
            `${telemetry.pressure ?? "--"} PSI`;

    }


    // -------------------------
    // DEVICE ID
    // -------------------------

    const metaValues =
        document.querySelectorAll(".machine-meta b");

    if (metaValues.length >= 1) {

        metaValues[0].textContent =
            telemetry.device_id || "factory-machine-01";

    }


    // -------------------------
    // LAST UPDATE
    // -------------------------

    if (metaValues.length >= 2 && telemetry.timestamp) {

        const date = new Date(telemetry.timestamp);

        metaValues[1].textContent =
            date.toLocaleTimeString();

    }


    // -------------------------
    // TEMPERATURE BAR
    // -------------------------

    const tempBar =
        document.querySelector(".bar.temp");

    if (
        tempBar &&
        telemetry.temperature !== undefined
    ) {

        let percentage =
            (Number(telemetry.temperature) / 110) * 100;

        percentage =
            Math.min(Math.max(percentage, 0), 100);

        tempBar.style.width =
            percentage + "%";

    }


    // -------------------------
    // PRESSURE BAR
    // -------------------------

    const pressureBar =
        document.querySelector(".bar.pressure");

    if (
        pressureBar &&
        telemetry.pressure !== undefined
    ) {

        let percentage =
            (Number(telemetry.pressure) / 50) * 100;

        percentage =
            Math.min(Math.max(percentage, 0), 100);

        pressureBar.style.width =
            percentage + "%";

    }


    // -------------------------
    // WARNING COUNT
    // -------------------------

    const statCards =
        document.querySelectorAll(".stat-card");

    if (statCards.length >= 3) {

        const warningValue =
            statCards[2].querySelector("h2");

        if (warningValue) {

            warningValue.textContent =
                Number(telemetry.temperature) > 80
                    ? "01"
                    : "00";

        }

    }


    // -------------------------
    // ACTIVE ALERTS
    // -------------------------

    if (statCards.length >= 4) {

        const activeAlertValue =
            statCards[3].querySelector("h2");

        if (activeAlertValue) {

            activeAlertValue.textContent =
                String(alerts.length).padStart(2, "0");

        }

    }


    // -------------------------
    // ONLINE DEVICES
    // -------------------------

    if (statCards.length >= 2) {

        const onlineValue =
            statCards[1].querySelector("h2");

        if (onlineValue) {

            onlineValue.textContent =
                machine.status === "Online"
                    ? "01"
                    : "00";

        }

    }


    // -------------------------
    // RECENT ALERT
    // -------------------------

    const alertContainer =
        document.querySelector(".alert-panel .alert-item");

    if (
        alertContainer &&
        alerts.length > 0
    ) {

        const latestAlert = alerts[0];

        alertContainer.innerHTML = `

            <div class="alert-icon">⚠</div>

            <div class="alert-details">

                <strong>
                    ${latestAlert.alert || "System Alert"}
                </strong>

                <span>
                    ${latestAlert.device_id || "Unknown Device"}
                </span>

                <small>
                    ${latestAlert.message || "Attention required"}
                </small>

            </div>

            <div class="alert-time">
                Now
            </div>

        `;

    }

}


// -------------------------
// INITIAL LOAD
// -------------------------

loadDashboard();


// -------------------------
// AUTO REFRESH EVERY 5 SEC
// -------------------------

setInterval(loadDashboard, 5000);