import streamlit as st
import matplotlib.pyplot as plt
import random
import psutil
import boto3
import time
import threading

# AWS setup
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
sns_client = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:992382729083:Node-Application-Testing"

def send_metrics_to_cloudwatch(cpu_usage, memory_usage, algorithm):
    cloudwatch.put_metric_data(
        Namespace='SortingApp',
        MetricData=[
            {
                'MetricName': 'CPU_Usage',
                'Dimensions': [{'Name': 'Algorithm', 'Value': algorithm}],
                'Unit': 'Percent',
                'Value': cpu_usage
            },
            {
                'MetricName': 'Memory_Usage',
                'Dimensions': [{'Name': 'Algorithm', 'Value': algorithm}],
                'Unit': 'Megabytes',
                'Value': memory_usage
            }
        ]
    )

def send_sns_notification(subject, message):
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )

def monitor_utilization(cpu_data, memory_data, stop_event):
    """Monitor CPU and memory usage."""
    while not stop_event.is_set():
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # in MB
        cpu_data.append(cpu_usage)
        memory_data.append(memory_usage)

        send_metrics_to_cloudwatch(cpu_usage, memory_usage, "Monitoring")

        if cpu_usage > 85:
            send_sns_notification(
                subject="High CPU Usage Alert",
                message=f"CPU usage exceeded 85%. Current usage: {cpu_usage}%"
            )

        time.sleep(1)  # Sample every second

def update_plot(data, bar_rects, iteration):
    for rect, val in zip(bar_rects, data):
        rect.set_height(val)

def bubble_sort_visualizer(data, cpu_data, memory_data):
    n = len(data)
    fig, ax = plt.subplots()
    bar_rects = ax.bar(range(len(data)), data, align="edge")
    ax.set_xlim(0, n)
    ax.set_ylim(0, int(1.1 * max(data)))

    iteration = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]  # Swap
            iteration += 1
            update_plot(data, bar_rects, iteration)
            plt.title(f'Sorting Algorithm Visualization | Iteration: {iteration}')
            st.pyplot(fig)
            time.sleep(0.1)  # Control the speed of sorting

    plt.close(fig)  # Close the plot after sorting

def main():
    st.title("Sorting Algorithm Visualizer with Utilization Monitoring")

    # Lists to store CPU and memory data
    cpu_data = []
    memory_data = []
    stop_event = threading.Event()

    data_size = st.slider("Select the size of data to sort:", 5, 100, 30)
    data = random.sample(range(1, 100), data_size)

    st.write(f"Original Data: {data}")

    algorithm = st.selectbox("Choose a sorting algorithm:", ["Bubble Sort"])

    if st.button("Run"):
        # Start the monitoring in a separate thread
        monitoring_thread = threading.Thread(target=monitor_utilization, args=(cpu_data, memory_data, stop_event), daemon=True)
        monitoring_thread.start()

        if algorithm == 'Bubble Sort':
            bubble_sort_visualizer(data, cpu_data, memory_data)

        # Stop monitoring after sorting is done
        stop_event.set()

        # Display CPU and memory utilization data as line charts
        st.subheader("System Utilization")
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))

        ax[0].plot(cpu_data, color='orange', label='CPU Usage (%)')
        ax[0].set_title('CPU Utilization')
        ax[0].set_xlabel('Time (seconds)')
        ax[0].set_ylabel('CPU Usage (%)')
        ax[0].legend()
        ax[0].grid()

        ax[1].plot(memory_data, color='green', label='Memory Usage (MB)')
        ax[1].set_title('Memory Utilization')
        ax[1].set_xlabel('Time (seconds)')
        ax[1].set_ylabel('Memory Usage (MB)')
        ax[1].legend()
        ax[1].grid()

        st.pyplot(fig)

if __name__ == "__main__":
    main()
