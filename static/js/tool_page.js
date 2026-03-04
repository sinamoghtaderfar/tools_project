const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("file-list");

function updateFileList() {
    const files = Array.from(fileInput.files);
    if (!files.length) {
        fileList.textContent = "No files selected.";
        return;
    }

    let names = [];
    for (let f of files) {
        if (f.size > MAX_FILE_SIZE) {
            alert(`File ${f.name} is too large! Max size: 5 MB.`);
            fileInput.value = "";
            fileList.textContent = "No files selected.";
            return;
        }
        names.push(f.name);
    }

    if (names.length === 1) {
        fileList.textContent = `Selected: ${names[0]}`;
    } else {
        fileList.textContent = `Selected ${names.length} files: ${names.join(", ")}`;
    }
}

function checkFiles() {
    if (!fileInput.files.length) {
        alert("Please select at least one file.");
        return false;
    }
    return true;
}

// Initial update
updateFileList();
