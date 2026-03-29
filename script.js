function robotTyping() {

    const element = document.getElementById("robot-text");
    const user = element.getAttribute("data-user");

    const message = "Hi " + user + " 👋 I am Karen, your ERP assistant";

    let i = 0;

    function typing() {
        if (i < message.length) {
            element.innerHTML += message.charAt(i);
            i++;
            setTimeout(typing, 60);
        }
    }

    typing();
}

let step = 0;
let studentName = "";
let year = "";
let branch = "";
let queryType = "";
let subject = "";

window.onload = function () {

    robotTyping();

    addMessage("🤖 : Hii 👋 Please enter the student name.");
};

function addMessage(message) {
    let chatBox = document.getElementById("chat-box");
    let div = document.createElement("div");
    div.className = "card";
    div.innerHTML = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    let input = document.getElementById("user-input");
    let text = input.value.toLowerCase().trim();
    input.value = "";

    if (text === "") return;

    addMessage("You: " + text);

    // STEP 0 → Student Name
    if (step === 0) {
        studentName = text;
        addMessage("🤖 : Please enter the year (1st year / 2nd year).");
        step = 1;
        return;
    }

    // STEP 1 → Year
    if (step === 1) {
        year = text;
        addMessage("🤖 : Please enter the branch (CSE / AIDS).");
        step = 2;
        return;
    }

    // STEP 2 → Branch
    if (step === 2) {
        branch = text;
        addMessage("🤖 : Do you want attendance, marks or exam dates?");
        step = 3;
        return;
    }

    // STEP 3 → Query Type
    if (step === 3) {

        if (text.includes("attendance")) {
            queryType = "attendance";
        } 
        else if (text.includes("marks")) {
            queryType = "marks";
        } 
        else if (text.includes("exam")) {
            queryType = "exam";
        } 
        else {
            addMessage("🤖 : Please type attendance, marks or exam dates.");
            return;
        }

        addMessage("🤖 : Please specify the subject.");
        step = 4;
        return;
    }

    // STEP 4 → Subject + Fetch
    if (step === 4) {
        subject = text;

        addMessage("🤖 : Fetching details... ⏳");

        fetch("/get_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                student: studentName,
                year: year,
                branch: branch,
                type: queryType,
                subject: subject
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.result) {
                addMessage("✅ Result: " + data.result);

                // ✅ SHOW DOWNLOAD BUTTON
                addMessage(`
                    <button onclick="downloadPDF()" 
                    style="margin-top:10px;padding:8px 15px;
                    border:none;border-radius:8px;
                    background:#4CAF50;color:white;
                    cursor:pointer;">
                    📄 Download Full Report
                    </button>
                `);
            } 
            else {
                addMessage("❌ Error: " + data.error);
            }

            addMessage("🤖 : You can enter another student name to continue.");

            // ⚠ DO NOT RESET HERE
            // We will reset only after download or new input

        })
        .catch(error => {
            addMessage("❌ Server Error. Please try again.");
            console.error(error);
        });

        step = 0;  // Allow new student entry
    }
}

// ✅ DOWNLOAD FUNCTION (WORKING)
function downloadPDF() {

    fetch("/download_report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student: studentName,
            year: year,
            branch: branch
        })
    })
    .then(response => response.blob())
    .then(blob => {

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = studentName + "_report.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();

    })
    .catch(error => {
        console.error("Download error:", error);
    });
}

// ENTER KEY SUPPORT
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("user-input");

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});