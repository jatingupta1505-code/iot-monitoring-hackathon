\# FactoryIQ – Cloud-Based Real-Time IoT Monitoring Platform



\## 📌 Project Overview



FactoryIQ is a cloud-based real-time IoT monitoring platform designed to monitor industrial machines and detect abnormal operating conditions.



The system simulates factory machine sensor data such as temperature and pressure, securely sends the data to AWS IoT Core using MQTT, processes the telemetry using AWS Lambda, stores the data in Amazon DynamoDB, generates alerts through Amazon SNS, and displays the information through a web-based monitoring dashboard.



\---



\## 🎯 Problem Statement



Industrial machines continuously generate sensor data such as:



\* Temperature

\* Pressure

\* Machine status



Manually monitoring this data can make it difficult to identify abnormal conditions quickly.



FactoryIQ provides a cloud-based solution that:



\* Collects real-time machine telemetry

\* Detects abnormal temperature conditions

\* Stores telemetry and alert records

\* Sends email notifications

\* Displays machine status through a web dashboard



\---



\## 🏗️ System Architecture



```text

Python IoT Simulator

&#x20;       │

&#x20;       │ MQTT

&#x20;       ▼

AWS IoT Core

&#x20;       │

&#x20;       │ IoT Rule

&#x20;       ▼

IoTMonitoringProcessor Lambda

&#x20;       │

&#x20;       ├──────────────► FactoryTelemetry DynamoDB

&#x20;       │

&#x20;       ├──────────────► FactoryAlerts DynamoDB

&#x20;       │

&#x20;       └──────────────► Amazon SNS

&#x20;                             │

&#x20;                             ▼

&#x20;                        Email Alert



FactoryIQ Dashboard

&#x20;       │

&#x20;       ▼

API Gateway

&#x20;       │

&#x20;       ▼

FactoryDashboardAPI Lambda

&#x20;       │

&#x20;       ▼

Amazon DynamoDB

```



\---



\## ☁️ AWS Services Used



| AWS Service        | Purpose                                    |

| ------------------ | ------------------------------------------ |

| AWS IoT Core       | Secure MQTT communication with IoT devices |

| AWS IoT Thing      | Represents the factory machine             |

| AWS IoT Policy     | Controls device permissions                |

| AWS Lambda         | Processes telemetry and generates alerts   |

| Amazon DynamoDB    | Stores telemetry and alert records         |

| Amazon SNS         | Sends email notifications                  |

| Amazon API Gateway | Provides API access to dashboard           |

| IAM                | Controls AWS resource permissions          |

| CloudWatch         | Lambda monitoring and logs                 |



\---



\## 🔄 Data Flow



1\. The Python simulator generates machine telemetry.

2\. Telemetry is published using the MQTT protocol.

3\. AWS IoT Core receives the telemetry.

4\. An IoT Rule forwards the message to Lambda.

5\. `IoTMonitoringProcessor` processes the telemetry.

6\. Temperature values above the configured threshold generate a warning.

7\. Telemetry is stored in `FactoryTelemetry`.

8\. Alert records are stored in `FactoryAlerts`.

9\. Amazon SNS sends an email notification for high-temperature conditions.

10\. API Gateway exposes the dashboard API.

11\. `FactoryDashboardAPI` retrieves the latest telemetry and alerts.

12\. The FactoryIQ web dashboard displays the machine status and readings.



\---



\## 🚨 Alert Logic



The current prototype uses an 80°C temperature threshold.



```text

Temperature > 80°C

&#x20;       ↓

HIGH TEMPERATURE

&#x20;       ↓

Store Alert in DynamoDB

&#x20;       ↓

Send SNS Notification

```



Temperature at or below the threshold is treated as normal.



\---



\## 📁 Project Structure



```text

iot-monitoring-hackathon/

│

├── dashboard/

│   ├── index.html

│   ├── style.css

│   └── script.js

│

├── simulator/

│   └── simulator.py

│

├── lambda/

│   ├── IoTMonitoringProcessor/

│   │   └── lambda\_function.py

│   │

│   └── FactoryDashboardAPI/

│       └── lambda\_function.py

│

├── docs/

│   └── architecture.png

│

├── .gitignore

└── README.md

```



\---



\## 🖥️ Dashboard



The FactoryIQ dashboard provides:



\* Total devices

\* Online device status

\* Warning status

\* Active alerts

\* Machine temperature

\* Machine pressure

\* Recent alerts

\* Live telemetry information

\* AWS cloud connection status



\---



\## 🛠️ Local Setup



\### 1. Clone the repository



```bash

git clone https://github.com/jatingupta1505-code/iot-monitoring-hackathon.git

cd iot-monitoring-hackathon

```



\### 2. Install Python dependencies



```bash

py -m pip install awsiotsdk

```



\### 3. Configure AWS IoT credentials



The simulator requires:



\* AWS IoT endpoint

\* Device certificate

\* Private key

\* Amazon Root CA



\*\*Important:\*\* AWS IoT certificates and private keys are intentionally excluded from this repository for security reasons.



Update the required paths and endpoint in `simulator/simulator.py`.



\### 4. Run the simulator



```bash

cd simulator

py simulator.py

```



The simulator publishes telemetry every few seconds.



\### 5. Run the dashboard locally



Open another CMD window:



```bash

cd dashboard

py -m http.server 8000

```



Then open:



```text

http://localhost:8000/index.html

```



\---



\## 🔐 Security



Sensitive AWS credentials are not included in this repository.



The following files are excluded using `.gitignore`:



```text

\*.pem

\*.pem.crt

\*.key

.env

venv/

```



Never upload private AWS IoT keys or certificates to GitHub.



\---



\## 📊 Current Prototype



The prototype supports:



\* Simulated IoT machine data

\* MQTT telemetry ingestion

\* AWS IoT Core

\* Serverless processing

\* DynamoDB storage

\* Temperature threshold detection

\* Alert storage

\* SNS email notifications

\* API-based dashboard

\* Machine online/offline detection

\* Cloud-based monitoring



\---



\## 🚀 Future Improvements



\* Support multiple factory machines

\* Add real-time charts

\* Add machine filtering

\* Add alert acknowledgement

\* Add configurable thresholds

\* Add device online/offline tracking

\* Add malformed message handling

\* Add authentication for dashboard users

\* Add CloudWatch monitoring and metrics

\* Improve alert cooldown/debouncing

\* Deploy dashboard using Amazon S3 and CloudFront



\---



\## 🧑‍💻 Technologies



\*\*Programming\*\*



\* Python

\* HTML

\* CSS

\* JavaScript



\*\*Cloud\*\*



\* AWS IoT Core

\* AWS Lambda

\* Amazon DynamoDB

\* Amazon SNS

\* Amazon API Gateway

\* AWS IAM

\* Amazon CloudWatch



\*\*Communication\*\*



\* MQTT

\* REST API



\---



\## 👨‍💻 Project



\*\*FactoryIQ – Cloud-Based Real-Time IoT Monitoring Platform\*\*



Built as a cloud computing hackathon project.



