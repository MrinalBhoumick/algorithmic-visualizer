Here's an updated README to reflect the integration of Streamlit for a more interactive user interface.

---

# Sorting Algorithm Visualizer with System Utilization Monitoring

This application visualizes various sorting algorithms using Streamlit and Matplotlib while simultaneously monitoring system CPU and memory utilization. Metrics are sent to AWS CloudWatch, and alerts can be triggered via Amazon SNS.

## Features

- Interactive web interface for visualizing sorting algorithms:
  - Bubble Sort
  - (Additional algorithms can be added easily)
- Real-time monitoring of system CPU and memory utilization.
- Sends utilization metrics to AWS CloudWatch.
- SNS notifications for high CPU usage alerts.
- Graphical plots for sorting visualizations and system utilization.

## Prerequisites

- Python 3.x
- Required libraries:
  - `streamlit`
  - `matplotlib`
  - `psutil`
  - `boto3`
- AWS credentials configured with permissions for CloudWatch and SNS.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required packages:**
   ```bash
   pip install streamlit matplotlib psutil boto3
   ```

3. **Set up AWS credentials:**
   Ensure your AWS credentials are configured in your environment. This can typically be done via the `~/.aws/credentials` file or by setting environment variables.

4. **Create an SNS Topic:**
   Create an SNS topic in the AWS Management Console and replace the `SNS_TOPIC_ARN` variable in the code with your SNS topic ARN.

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run your_script.py
   ```

2. Access the web interface in your browser (usually at `http://localhost:8501`).

3. Choose a sorting algorithm and monitor system utilization:
   - Select a sorting algorithm from the dropdown menu.
   - Click the "Run" button to start the visualization.
   - Monitor CPU and memory usage in real-time.

## Code Overview

- **send_metrics_to_cloudwatch**: Sends CPU and memory metrics to AWS CloudWatch.
- **send_sns_notification**: Sends an alert to the configured SNS topic if CPU usage exceeds 85%.
- **update_plot**: Updates the sorting visualization and sends metrics to CloudWatch.
- **bubble_sort_visualizer**: Visualizes the Bubble Sort algorithm.
- **monitor_utilization**: Continuously monitors and plots CPU and memory usage.
- **main**: The entry point of the Streamlit application where user interaction takes place.

## Contribution

Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
