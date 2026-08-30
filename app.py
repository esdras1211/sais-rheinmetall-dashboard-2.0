```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rheinmetall Geopolitical Risk Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background-color: #1E2229;
            color: #FFFFFF;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        .card-bg {
            background-color: #252A34;
            border: 1px solid #2D323E;
        }
        .metric-label {
            color: #A0A5B5;
            font-size: 0.875rem;
            font-weight: 500;
            letter-spacing: 0.05em;
        }
        .metric-value {
            color: #FFFFFF;
            font-size: 2rem;
            font-weight: 700;
        }
        .status-stable { background-color: #2ECC71; color: #FFFFFF; }
        .status-warning { background-color: #FFD13B; color: #1E2229; }
        .status-critical { background-color: #FF4B4B; color: #FFFFFF; }
        .scenario-btn {
            transition: all 0.2s ease;
            border: 2px solid #3D4352;
        }
        .scenario-btn:hover {
            border-color: #FFD13B;
            transform: translateY(-2px);
        }
        .scenario-btn.active {
            background-color: #FFD13B;
            color: #1E2229;
            border-color: #FFD13B;
        }
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        th {
            background-color: #1E2229;
            color: #A0A5B5;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            padding: 12px 16px;
            text-align: left;
            position: sticky;
            top: 0;
        }
        td {
            padding: 12px 16px;
            border-bottom: 1px solid #2D323E;
            font-size: 0.875rem;
        }
        tr:hover td {
            background-color: #2D323E;
        }
        .gauge-container {
            position: relative;
            width: 100%;
            height: 280px;
        }
    </style>
</head>
<body class="p-6">
    <div class="max-w-[1920px] mx-auto">
        <!-- TOP ROW: HEADER & KPI PANEL -->
        <div class="mb-6">
            <h1 class="text-3xl font-bold mb-6 tracking-tight">RHEINMETALL GEOPOLITICAL RISK ASSESSMENT: €80B BACKLOG BOTTLENECKS</h1>
            
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
                <!-- Total Backlog KPI -->
                <div class="card-bg rounded-lg p-6">
                    <div class="metric-label mb-2">TOTAL BACKLOG VOLUME</div>
                    <div class="metric-value" id="totalBacklog">€80.0 Billion</div>
                </div>
                
                <!-- Critical Alerts KPI -->
                <div class="card-bg rounded-lg p-6">
                    <div class="metric-label mb-2">ACTIVE CRITICAL ALERTS</div>
                    <div class="metric-value text-red-500" id="criticalAlerts">0 Breached</div>
                </div>
                
                <!-- Scenario Selector -->
                <div class="card-bg rounded-lg p-6">
                    <div class="metric-label mb-3">ENERGY SHOCK SCENARIO SIMULATION</div>
                    <div class="grid grid-cols-2 gap-2" id="scenarioButtons"></div>
                </div>
            </div>
        </div>

        <!-- MIDDLE ROW: OPERATIONAL MATRIX -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <!-- Left: Asset Profiles -->
            <div class="card-bg rounded-lg p-6">
                <h2 class="text-xl font-bold mb-4">Asset Profiles: Global Capacity Tracking</h2>
                <div class="overflow-auto max-h-[400px]">
                    <table>
                        <thead>
                            <tr>
                                <th>Facility</th>
                                <th>Country</th>
                                <th>Output Category</th>
                                <th>Backlog (B€)</th>
                                <th>Utilization</th>
                            </tr>
                        </thead>
                        <tbody id="assetTable"></tbody>
                    </table>
                </div>
            </div>

            <!-- Right: Supply Chain Bottleneck Matrix -->
            <div class="card-bg rounded-lg p-6">
                <h2 class="text-xl font-bold mb-4">Supply Chain & Energy Signpost Matrix</h2>
                <div class="overflow-auto max-h-[400px]">
                    <table>
                        <thead>
                            <tr>
                                <th>Facility</th>
                                <th>Bottleneck Metric</th>
                                <th>Current</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="bottleneckTable"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- BOTTOM ROW: TREND ANALYSIS & RISK GAUGE -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Historical Trend Chart -->
            <div class="card-bg rounded-lg p-6 lg:col-span-2">
                <h2 class="text-xl font-bold mb-4">Annual Backlog Accumulation Layer (2022 - 2026 Trace)</h2>
                <canvas id="trendChart" height="100"></canvas>
            </div>

            <!-- Risk Exposure Gauge -->
            <div class="card-bg rounded-lg p-6">
                <h2 class="text-xl font-bold mb-4">Scenario Risk Capital Exposure</h2>
                <div class="gauge-container">
                    <canvas id="gaugeChart"></canvas>
                </div>
                <div class="text-center mt-4">
                    <div class="metric-label">BACKLOG AT RISK (BILLION EUR)</div>
                    <div class="text-3xl font-bold" id="riskValue">€0.0</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // DATA LAYER
        const Asset_Dim = [
            { Facility_ID: "FAC_01", Facility_Name: "Unterlüß Hub", Country: "Germany", Latitude: 52.8512, Longitude: 10.2915, Primary_Output_Category: "Ammunition & Weapons", Sovereign_Risk_Score: 1.2 },
            { Facility_ID: "FAC_02", Facility_Name: "Kassel Plant", Country: "Germany", Latitude: 51.3127, Longitude: 9.4797, Primary_Output_Category: "Tactical Wheeled Vehicles", Sovereign_Risk_Score: 1.2 },
            { Facility_ID: "FAC_03", Facility_Name: "Zalaegerszeg Complex", Country: "Hungary", Latitude: 46.8416, Longitude: 16.8438, Primary_Output_Category: "Lynx Infantry Fighting Vehicles", Sovereign_Risk_Score: 2.8 },
            { Facility_ID: "FAC_04", Facility_Name: "Várpalota Ammunition", Country: "Hungary", Latitude: 47.1994, Longitude: 18.1394, Primary_Output_Category: "Large Caliber Shells", Sovereign_Risk_Score: 2.8 },
            { Facility_ID: "FAC_05", Facility_Name: "Somerset West Node", Country: "South Africa", Latitude: -34.0514, Longitude: 18.8417, Primary_Output_Category: "Propellants & Energetics", Sovereign_Risk_Score: 3.9 },
            { Facility_ID: "FAC_06", Facility_Name: "Redbank Facility", Country: "Australia", Latitude: -27.5994, Longitude: 152.8804, Primary_Output_Category: "Boxer CRV Integration", Sovereign_Risk_Score: 1.1 },
            { Facility_ID: "FAC_07", Facility_Name: "Ukraine JV Facility", Country: "Ukraine", Latitude: 48.3794, Longitude: 31.1656, Primary_Output_Category: "Armored Vehicle MRO & Production", Sovereign_Risk_Score: 4.8 }
        ];

        const Backlog_Fact = [
            { Fact_ID: "BKL_101", Facility_ID: "FAC_01", Division: "Weapons & Ammo", Backlog_Allocated_Billions: 22.4, Capacity_Utilization_Pct: 0.95 },
            { Fact_ID: "BKL_102", Facility_ID: "FAC_02", Division: "Vehicle Systems", Backlog_Allocated_Billions: 18.1, Capacity_Utilization_Pct: 0.88 },
            { Fact_ID: "BKL_103", Facility_ID: "FAC_03", Division: "Vehicle Systems", Backlog_Allocated_Billions: 12.5, Capacity_Utilization_Pct: 0.72 },
            { Fact_ID: "BKL_104", Facility_ID: "FAC_04", Division: "Weapons & Ammo", Backlog_Allocated_Billions: 14.2, Capacity_Utilization_Pct: 0.65 },
            { Fact_ID: "BKL_105", Facility_ID: "FAC_05", Division: "Weapons & Ammo", Backlog_Allocated_Billions: 5.8, Capacity_Utilization_Pct: 0.82 },
            { Fact_ID: "BKL_106", Facility_ID: "FAC_06", Division: "Vehicle Systems", Backlog_Allocated_Billions: 4.5, Capacity_Utilization_Pct: 0.55 },
            { Fact_ID: "BKL_107", Facility_ID: "FAC_07", Division: "Vehicle Systems", Backlog_Allocated_Billions: 2.5, Capacity_Utilization_Pct: 0.40 }
        ];

        const Backlog_History_Fact = [
            { History_ID: "HIS_201", Year: 2022, Division: "Weapons & Ammo", Historical_Backlog_Billions: 14.2, YOY_Growth_Rate: 0.00 },
            { History_ID: "HIS_202", Year: 2022, Division: "Vehicle Systems", Historical_Backlog_Billions: 12.5, YOY_Growth_Rate: 0.00 },
            { History_ID: "HIS_203", Year: 2023, Division: "Weapons & Ammo", Historical_Backlog_Billions: 19.8, YOY_Growth_Rate: 0.39 },
            { History_ID: "HIS_204", Year: 2023, Division: "Vehicle Systems", Historical_Backlog_Billions: 16.4, YOY_Growth_Rate: 0.31 },
            { History_ID: "HIS_205", Year: 2024, Division: "Weapons & Ammo", Historical_Backlog_Billions: 28.5, YOY_Growth_Rate: 0.44 },
            { History_ID: "HIS_206", Year: 2024, Division: "Vehicle Systems", Historical_Backlog_Billions: 22.1, YOY_Growth_Rate: 0.35 },
            { History_ID: "HIS_207", Year: 2025, Division: "Weapons & Ammo", Historical_Backlog_Billions: 38.2, YOY_Growth_Rate: 0.34 },
            { History_ID: "HIS_208", Year: 2025, Division: "Vehicle Systems", Historical_Backlog_Billions: 26.3, YOY_Growth_Rate: 0.19 },
            { History_ID: "HIS_209", Year: 2026, Division: "Weapons & Ammo", Historical_Backlog_Billions: 42.4, YOY_Growth_Rate: 0.11 },
            { History_ID: "HIS_210", Year: 2026, Division: "Vehicle Systems", Historical_Backlog_Billions: 37.6, YOY_Growth_Rate: 0.43 }
        ];

        const Supply_Energy_Fact = [
            { Metric_ID: "SIG_301", Facility_ID: "FAC_01", Bottleneck_Metric_Name: "Nitrocellulose Precursor Deficit", Current_Value: 38.5, Unit: "Pct", Green_Max: 10.0, Yellow_Max: 25.0, Red_Min: 25.01 },
            { Metric_ID: "SIG_302", Facility_ID: "FAC_05", Bottleneck_Metric_Name: "Propellant Powder Lead Times", Current_Value: 18.0, Unit: "Months", Green_Max: 6.0, Yellow_Max: 12.0, Red_Min: 12.01 },
            { Metric_ID: "SIG_303", Facility_ID: "FAC_04", Bottleneck_Metric_Name: "Parallel RDX Plant Delay", Current_Value: 120.0, Unit: "Days", Green_Max: 30.0, Yellow_Max: 90.0, Red_Min: 90.01 },
            { Metric_ID: "SIG_304", Facility_ID: "FAC_01", Bottleneck_Metric_Name: "Central European EEX Gas Spot", Current_Value: 58.4, Unit: "EUR/MWh", Green_Max: 35.0, Yellow_Max: 50.0, Red_Min: 50.01 },
            { Metric_ID: "SIG_305", Facility_ID: "FAC_05", Bottleneck_Metric_Name: "Eskom Load-Shedding Power Loss", Current_Value: 14.5, Unit: "Hours/Wk", Green_Max: 4.0, Yellow_Max: 10.0, Red_Min: 10.01 },
            { Metric_ID: "SIG_306", Facility_ID: "FAC_06", Bottleneck_Metric_Name: "Drewry Maritime Steel Transit Delay", Current_Value: 22.0, Unit: "Days", Green_Max: 7.0, Yellow_Max: 15.0, Red_Min: 15.01 },
            { Metric_ID: "SIG_307", Facility_ID: "FAC_07", Bottleneck_Metric_Name: "Warzone Kinetic Disruption Delay", Current_Value: 45.0, Unit: "Days", Green_Max: 5.0, Yellow_Max: 20.0, Red_Min: 20.01 }
        ];

        const Price_Shock_Dim = [
            { Shock_Scenario_ID: "SHK_01", Scenario_Label: "Baseline Operations", Gas_Threshold_Trigger: 0.0, Risk_Multiplier: 0.00 },
            { Shock_Scenario_ID: "SHK_02", Scenario_Label: "Elevated Grid Strain", Gas_Threshold_Trigger: 50.0, Risk_Multiplier: 0.15 },
            { Shock_Scenario_ID: "SHK_03", Scenario_Label: "Acute Curtailment", Gas_Threshold_Trigger: 75.0, Risk_Multiplier: 0.45 },
            { Shock_Scenario_ID: "SHK_04", Scenario_Label: "Systemic Energy Shock", Gas_Threshold_Trigger: 100.0, Risk_Multiplier: 0.80 }
        ];

        // STATE MANAGEMENT
        let currentScenario = Price_Shock_Dim[0];
        let trendChart = null;
        let gaugeChart = null;

        // RULE A: Risk Metric Aggregator
        function evaluateRiskStatus(metric) {
            const value = metric.Current_Value;
            if (value <= metric.Green_Max) {
                return { status: "Stable", color: "#2ECC71", class: "status-stable" };
            } else if (value <= metric.Yellow_Max) {
                return { status: "Warning", color: "#FFD13B", class: "status-warning" };
            } else {
                return { status: "Critical", color: "#FF4B4B", class: "status-critical" };
            }
        }

        // RULE B: Macro Scenario Simulation Engine
        function calculateRiskExposure(scenario) {
            const energyIntensiveFacilities = ["FAC_01", "FAC_04"];
            let directExposure = 0;
            let cascadingExposure = 0;

            Backlog_Fact.forEach(fact => {
                if (energyIntensiveFacilities.includes(fact.Facility_ID)) {
                    directExposure += fact.Backlog_Allocated_Billions * scenario.Risk_Multiplier;
                } else {
                    cascadingExposure += fact.Backlog_Allocated_Billions * (scenario.Risk_Multiplier * 0.20);
                }
            });

            return directExposure + cascadingExposure;
        }

        // UI RENDERING FUNCTIONS
        function renderScenarioButtons() {
            const container = document.getElementById('scenarioButtons');
            container.innerHTML = '';
            
            Price_Shock_Dim.forEach(scenario => {
                const btn = document.createElement('button');
                btn.className = `scenario-btn px-3 py-2 rounded text-xs font-semibold ${scenario.Shock_Scenario_ID === currentScenario.Shock_Scenario_ID ? 'active' : 'bg-transparent text-white'}`;
                btn.textContent = scenario.Scenario_Label;
                btn.onclick = () => selectScenario(scenario);
                container.appendChild(btn);
            });
        }

        function renderAssetTable() {
            const tbody = document.getElementById('assetTable');
            tbody.innerHTML = '';

            Asset_Dim.forEach(asset => {
                const backlog = Backlog_Fact.find(b => b.Facility_ID === asset.Facility_ID);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="font-medium">${asset.Facility_Name}</td>
                    <td>${asset.Country}</td>
                    <td class="text-sm">${asset.Primary_Output_Category}</td>
                    <td class="font-bold">€${backlog ? backlog.Backlog_Allocated_Billions.toFixed(1) : '0.0'}B</td>
                    <td>
                        <div class="flex items-center gap-2">
                            <div class="w-20 h-2 bg-gray-700 rounded-full overflow-hidden">
                                <div class="h-full bg-blue-500" style="width: ${backlog ? backlog.Capacity_Utilization_Pct * 100 : 0}%"></div>
                            </div>
                            <span class="text-xs">${backlog ? (backlog.Capacity_Utilization_Pct * 100).toFixed(0) : 0}%</span>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        function renderBottleneckTable() {
            const tbody = document.getElementById('bottleneckTable');
            tbody.innerHTML = '';
            let criticalCount = 0;

            Supply_Energy_Fact.forEach(metric => {
                const asset = Asset_Dim.find(a => a.Facility_ID === metric.Facility_ID);
                const riskEval = evaluateRiskStatus(metric);
                if (riskEval.status === "Critical") criticalCount++;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="font-medium">${asset ? asset.Facility_Name : metric.Facility_ID}</td>
                    <td class="text-sm">${metric.Bottleneck_Metric_Name}</td>
                    <td class="font-bold">${metric.Current_Value} ${metric.Unit}</td>
                    <td>
                        <span class="px-3 py-1 rounded-full text-xs font-bold ${riskEval.class}">
                            ${riskEval.status}
                        </span>
                    </td>
                `;
                tbody.appendChild(row);
            });

            document.getElementById('criticalAlerts').textContent = `${criticalCount} Breached`;
        }

        function renderTrendChart() {
            const ctx = document.getElementById('trendChart').getContext('2d');
            
            const years = [...new Set(Backlog_History_Fact.map(h => h.Year))].sort();
            const weaponsData = years.map(year => {
                const entry = Backlog_History_Fact.find(h => h.Year === year && h.Division === "Weapons & Ammo");
                return entry ? entry.Historical_Backlog_Billions : 0;
            });
            const vehiclesData = years.map(year => {
                const entry = Backlog_History_Fact.find(h => h.Year === year && h.Division === "Vehicle Systems");
                return entry ? entry.Historical_Backlog_Billions : 0;
            });
            const totalData = years.map((year, idx) => weaponsData[idx] + vehiclesData[idx]);

            if (trendChart) trendChart.destroy();

            trendChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: years,
                    datasets: [
                        {
                            label: 'Weapons & Ammo',
                            data: weaponsData,
                            backgroundColor: '#3B82F6',
                            borderWidth: 0
                        },
                        {
                            label: 'Vehicle Systems',
                            data: vehiclesData,
                            backgroundColor: '#8B5CF6',
                            borderWidth: 0
                        },
                        {
                            label: 'Total Trajectory',
                            data: totalData,
                            type: 'line',
                            borderColor: '#FFD13B',
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            pointRadius: 5,
                            pointBackgroundColor: '#FFD13B',
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: '#A0A5B5', font: { size: 11 } }
                        }
                    },
                    scales: {
                        x: {
                            stacked: true,
                            grid: { color: '#2D323E' },
                            ticks: { color: '#A0A5B5' }
                        },
                        y: {
                            stacked: true,
                            grid: { color: '#2D323E' },
                            ticks: { color: '#A0A5B5' },
                            title: { display: true, text: 'Backlog (Billion EUR)', color: '#A0A5B5' }
                        }
                    }
                }
            });
        }

        function renderGauge(riskValue) {
            const ctx = document.getElementById('gaugeChart').getContext('2d');
            const maxValue = 80;
            const percentage = (riskValue / maxValue) * 100;

            if (gaugeChart) gaugeChart.destroy();

            gaugeChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [riskValue, maxValue - riskValue],
                        backgroundColor: [
                            riskValue < 15 ? '#2ECC71' : riskValue < 35 ? '#FFD13B' : '#FF4B4B',
                            '#2D323E'
                        ],
                        borderWidth: 0,
                        circumference: 180,
                        rotation: 270
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    }
                }
            });

            document.getElementById('riskValue').textContent = `€${riskValue.toFixed(1)}B`;
        }

        function selectScenario(scenario) {
            currentScenario = scenario;
            renderScenarioButtons();
            const riskExposure = calculateRiskExposure(scenario);
            renderGauge(riskExposure);
        }

        // INITIALIZATION
        function init() {
            renderScenarioButtons();
            renderAssetTable();
            renderBottleneckTable();
            renderTrendChart();
            selectScenario(Price_Shock_Dim[0]);
        }

        init();
    </script>
</body>
</html>
```
