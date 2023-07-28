function deleteNote(id) {
  // Send a POST request to "/deleteNote" endpoint
  fetch("/deleteNote", {
    method: "POST",
    body: JSON.stringify({ id: id }), // JSON payload with id
  }).then((_res) => {
    // After the request is completed, redirect to the root URL ("/")
    window.location.href = "/";
  });
}