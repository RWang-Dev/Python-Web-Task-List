// Sends a POST request to the backend using the note Id that we have passed,
// Then, reloads the current page
function deleteNote(noteId) {
  fetch("/delete-note", {   // /delete-note deletes the note
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/"; // Refreshes the page after removing the note
  });
}
