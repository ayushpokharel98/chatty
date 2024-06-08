document.getElementById("toclick").addEventListener("click", function () {
    document.getElementById("toappear").classList.toggle("hidden");
})
document.getElementById("makeappearchat").addEventListener("click", function () {
    document.getElementById("toappearchat").classList.toggle("hidden");
})

document.getElementById("clickadd").addEventListener("click", function () {
    document.getElementById("clickaddappear").classList.toggle("hidden");
})
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("getpeopleform");
    const results = document.querySelector('.results');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const searchQuery = formData.get('search_query');

        try {
            // Make a request to the server to fetch search results
            const response = await fetch(`/search?query=${searchQuery}`);
            const data = await response.json();

            // Clear previous results
            results.innerHTML = '';

            if (data.length > 0) {
                // If results are found, display them
                data.forEach(result => {
                    const resultItem = document.createElement('div');
                    let reusltItem_item = document.createElement('div');
                    const hr_item = document.createElement('hr');
                    const button_item = document.createElement("button");
                    button_item.classList.add("flex-1");
                    button_item.innerHTML= '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M6.83333 11.8333C8.44167 11.8333 9.75 10.525 9.75 8.91667C9.75 7.30833 8.44167 6 6.83333 6C5.225 6 3.91667 7.30833 3.91667 8.91667C3.91667 10.525 5.225 11.8333 6.83333 11.8333ZM21 15.3333V12.8333H23.5V11.1667H21V8.66666H19.3333V11.1667H16.8333V12.8333H19.3333V15.3333H21ZM6.83333 13.2917C4.88333 13.2917 1 14.2667 1 16.2083V17.6667H12.6667V16.2083C12.6667 14.2667 8.78333 13.2917 6.83333 13.2917ZM6.83333 14.9583C5.34166 14.9583 3.65 15.5167 2.95 16H10.7167C10.0167 15.5167 8.325 14.9583 6.83333 14.9583ZM8.08333 8.91667C8.08333 8.225 7.525 7.66667 6.83333 7.66667C6.14167 7.66667 5.58333 8.225 5.58333 8.91667C5.58333 9.60833 6.14167 10.1667 6.83333 10.1667C7.525 10.1667 8.08333 9.60833 8.08333 8.91667ZM11 11.8333C12.6083 11.8333 13.9167 10.525 13.9167 8.91667C13.9167 7.30833 12.6083 6 11 6C10.8 6 10.6 6.01667 10.4083 6.05833C11.0417 6.84167 11.4167 7.83333 11.4167 8.91667C11.4167 10 11.025 10.9833 10.3917 11.7667C10.5917 11.8083 10.7917 11.8333 11 11.8333ZM14.3333 16.2083C14.3333 15.075 13.7667 14.1917 12.9333 13.5167C14.8 13.9083 16.8333 14.8 16.8333 16.2083V17.6667H14.3333V16.2083Z" fill="#000000"></path> </g></svg>'
                    hr_item.classList.add("mt-2", "w-full", "border", "border-gray-300");
                    resultItem.style = "display:flex; gap:0.5rem; padding:1rem";
                    resultItem.classList.add("hover:bg-gray-200", "hover:cursor-pointer");
                    let image = `<img src="${result.pp}" class="w-8 h-8 rounded-full">`;
                    reusltItem_item.innerHTML = `${result.username} ${image}`
                    reusltItem_item.classList.add("flex", "gap-2")
                    resultItem.appendChild(button_item);
                    resultItem.appendChild(reusltItem_item);
                    results.appendChild(resultItem);
                    results.appendChild(hr_item);
                    button_item.addEventListener("click", function(){
                        window.location.href = `add/${result.username}`
                    })
                });
            } else {
                // If no results are found, display a message
                results.textContent = 'No results found!';
            }
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    });
});