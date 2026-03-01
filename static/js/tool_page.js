const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("file-list");

fileInput.addEventListener("change", () => {
    const files = Array.from(fileInput.files);
    if (files.length === 0) {
        fileList.textContent = "No files selected.";
        return;
    }

    let names = [];
    for (let f of files) {
        if (f.size > MAX_FILE_SIZE) {
            alert(`File ${f.name} is too large! Maximum allowed size: 5 MB.`);
            fileInput.value = "";
            fileList.textContent = "No files selected.";
            return;
        }
        names.push(f.name);
    }

    fileList.textContent = names.join(", ");
});

function checkFiles() {
    if (!fileInput.files.length) {
        alert("Please select at least one file.");
        return false;
    }
    return true;
}