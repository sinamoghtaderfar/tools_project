document.addEventListener("DOMContentLoaded", function () {
    const toolsGrid = document.getElementById("toolsGrid");
    allTools.forEach(tool => {
        const a = document.createElement("a");
        a.href = tool.url;
        a.className = "tool-card group relative bg-white rounded-2xl shadow-md p-6 hover:shadow-xl transition-all duration-200";
        a.innerHTML = `
            <div class="text-4xl mb-4">${tool.name === "Merge PDF" ? "📄" : tool.name === "Compress Image" ? "🖼️" : "🔄"}</div>
            <h3 class="text-xl font-semibold mb-2">${tool.name}</h3>
            <p class="text-gray-600 text-sm mb-4">
                ${tool.name === "Merge PDF" ? "Combine multiple PDF files into a single document." :
                  tool.name === "Compress Image" ? "Reduce image size without losing quality." :
                  "Convert PDF to Word, Excel, or Images instantly."}
            </p>
            <span class="text-blue-600 font-medium hover:underline">Use Tool →</span>
        `;
        toolsGrid.appendChild(a);
    });

    // Search Bar
    const searchInput = document.getElementById("toolSearch");
    const searchResults = document.getElementById("searchResults");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.toLowerCase();
        searchResults.innerHTML = "";

        if (!query) {
            searchResults.classList.add("hidden");
            return;
        }

        const filtered = allTools.filter(tool => tool.name.toLowerCase().includes(query));

        if (filtered.length === 0) {
            searchResults.innerHTML = '<div class="px-4 py-2 text-gray-500">No results found</div>';
        } else {
            filtered.forEach(tool => {
                const div = document.createElement("div");
                div.className = "px-4 py-2 hover:bg-blue-100 cursor-pointer";
                div.innerHTML = `<a href="${tool.url}" class="block text-gray-800">${tool.name}</a>`;
                searchResults.appendChild(div);
            });
        }

        searchResults.classList.remove("hidden");
    });

    document.addEventListener("click", function (e) {
        if (!searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.classList.add("hidden");
        }
    });
});