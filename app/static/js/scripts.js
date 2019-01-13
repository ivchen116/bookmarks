// Empty JS for your own code to be here
var showEditModal = function (id) {
        $("#editModal").load("/sedit/" + id, function () {
            $("#editModal").modal('show');
        })
}
