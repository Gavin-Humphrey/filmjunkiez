// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;



const image = document.querySelector('.filmListFilm__image img');

if (image.naturalWidth < 250 && image.naturalHeight < 150) {
  image.style.objectFit = 'contain';
} else {
  image.style.objectFit = 'cover';
}


///Announcement
// JavaScript for updating announcement content
function updateAnnouncement(message) {
  var announcementBar = document.getElementById('announcementBar');
  announcementBar.innerText = message;
}
