// Change number of forms in management form for validation the formsset in backend
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('id_form-TOTAL_FORMS').value = $('#fixture_id').length;
});