function openDeleteModal(id, title, contentType) {
    const deleteForm = document.getElementById('deleteForm');
    let content = `Are you sure you want to delete the note "${title}"? It will be deleted permanently.`;
    if (contentType === 'notebook') {
        deleteForm.action = `/notebook/${id}/delete/`;
        content = `Are you sure you want to delete the notebook "${title}"? All notes inside it will be deleted permanently.`;
    }else deleteForm.action = `/note/delete/${id}/`;
    const modalText = document.getElementById('deleteModalText');
    modalText.textContent = content;
    document.getElementById('globalDeleteModal').classList.remove('hidden');
}

function closeDeleteModal() {
    document.getElementById('globalDeleteModal').classList.add('hidden');
}
