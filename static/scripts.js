// retrieve the sorting dropdown
const dropdown = document.getElementById('sort');

/** 
 * Automatically sets the selected sorting option in the dropdown based on the URL parameter.
 */
(() => {
    // parse the URL parameter
    const searchParams= new URLSearchParams(window.location.search);
    const sortValue = searchParams.get('sort');
    // set the selected sorting option in the dropdown, if valid
    if (sortValue && Array.from(dropdown.options).some(option => option.value === sortValue)) {
        dropdown.value = sortValue;
    }
})(); 

/** 
 * Redirects the user to the homepage with a specified sorting option.
 */
function dropdownRedirect() {
    window.location.href = '/?sort=' + dropdown.value;
}
