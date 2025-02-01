// Accessing the video element and setting up webcam
const video = document.getElementById("video");
const stopButton = document.getElementById("stop-btn");
const attendanceTableBody = document.querySelector("#attendance-table tbody");

let videoStream;

// Start the video stream when the page loads
window.addEventListener("load", async () => {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = videoStream;
    } catch (err) {
        alert("Unable to access the camera: " + err);
    }
});

// Handle the "Stop Attendance" button click to stop the webcam feed
stopButton.addEventListener("click", () => {
    if (videoStream) {
        const tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());
    }
    video.srcObject = null;
    alert("Attendance process stopped.");
});

// Dummy function to simulate marking attendance
function markAttendance(name) {
    const currentTime = new Date().toLocaleTimeString();
    const row = document.createElement("tr");
    const nameCell = document.createElement("td");
    const timeCell = document.createElement("td");

    nameCell.textContent = name;
    timeCell.textContent = currentTime;

    row.appendChild(nameCell);
    row.appendChild(timeCell);

    attendanceTableBody.appendChild(row);
}

// For simulation, we'll mark attendance for two names after 3 seconds
setTimeout(() => markAttendance("Anjali"), 3000);
setTimeout(() => markAttendance("Anjuu"), 6000);
