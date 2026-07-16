async function addRecord() {

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if (name === "" || email === "" || phone === "") {
        document.getElementById("message").innerHTML = "Please fill all fields.";
        return;
    }

    const response = await fetch("/add", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name,
            email: email,
            phone: phone
        })

    });

    const data = await response.json();

    document.getElementById("message").innerHTML = data.message;

    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phone").value = "";

    loadRecords();
    loadStats();

}

async function loadRecords() {

    const response = await fetch("/records");

    const records = await response.json();

    let html = "";

    records.forEach(record => {

        html += `

        <tr>

            <td>${record.id}</td>
            <td>${record.name}</td>
            <td>${record.email}</td>
            <td>${record.phone}</td>
            <td>${record.created_at}</td>

            <td>

                <button class="deleteBtn"
                onclick="deleteRecord(${record.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("tableData").innerHTML = html;

}

async function deleteRecord(id) {

    if (!confirm("Delete this record?")) {
        return;
    }

    await fetch("/delete/" + id, {

        method: "DELETE"

    });

    loadRecords();
    loadStats();

}

async function searchRecord() {

    const keyword = document.getElementById("search").value;

    const response = await fetch("/search?q=" + encodeURIComponent(keyword));

    const records = await response.json();

    let html = "";

    records.forEach(record => {

        html += `

        <tr>

            <td>${record.id}</td>
            <td>${record.name}</td>
            <td>${record.email}</td>
            <td>${record.phone}</td>
            <td>${record.created_at}</td>

            <td>

                <button class="deleteBtn"
                onclick="deleteRecord(${record.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

    document.getElementById("tableData").innerHTML = html;

}

async function loadStats() {

    const response = await fetch("/stats");

    const stats = await response.json();

    document.getElementById("total").innerHTML =
        stats.total_records;

    document.getElementById("duplicate").innerHTML =
        stats.duplicates_blocked;

    document.getElementById("falsePositive").innerHTML =
        stats.false_positives;

}

window.onload = function () {

    loadRecords();
    loadStats();

};