document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#date_of_grant", {
    dateFormat: "Y-m-d",
    allowInput: false,
  });

  document.querySelector("form").addEventListener("submit", function (e) {
    let fecha = document.getElementById("date_of_grant").value;
    if (!fecha) {
      alert("Por favor, selecciona una fecha.");
      e.preventDefault();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/creditlist")
    .then((response) => response.json())
    .then((data) => {
      const tbody = document.getElementById("credittable");
      tbody.innerHTML = ""; // Limpia el tbody antes de insertar los datos

      data.forEach((credito) => {
        let row = document.createElement("tr");

        row.innerHTML = `
                    <td>${credito.id}</td>
                    <td><input type="text" class="form-control" value="${credito.cliente}" disabled></td>
                    <td><input type="number" class="form-control" value="${credito.monto}" disabled></td>
                    <td><input type="number" class="form-control" value="${credito.tasa_interes}" disabled></td>
                    <td><input type="number" class="form-control" value="${credito.plazo}" disabled></td>
                    <td><input type="date" class="form-control" value="${credito.fecha_otorgamiento}" disabled></td>
                    <td>
                        <button class="btn btn-warning btn-sm edit-btn">Editar</button>
                        <button class="btn btn-success btn-sm save-btn" style="display:none;">Guardar</button>
                        <button class="btn btn-danger btn-sm delete-btn">Borrar</button>
                    </td>
                `;

        // Agregar eventos a los botones
        row
          .querySelector(".edit-btn")
          .addEventListener("click", () => toggleEdit(row, true));
        row
          .querySelector(".save-btn")
          .addEventListener("click", () => saveCredit(row, credito.id));
        row
          .querySelector(".delete-btn")
          .addEventListener("click", () => deleteCredit(credito.id));

        tbody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error al cargar créditos:", error));
});

// Habilitar // desahibiliar edicion de datos
function toggleEdit(row, enable) {
  const inputs = row.querySelectorAll("input");
  const editBtn = row.querySelector(".edit-btn");
  const saveBtn = row.querySelector(".save-btn");

  inputs.forEach((input) => (input.disabled = !enable));
  editBtn.style.display = enable ? "none" : "inline-block";
  saveBtn.style.display = enable ? "inline-block" : "none";
}

// Actualizar datos 
function saveCredit(row, id) {
  const inputs = row.querySelectorAll("input");
  const updatedData = {
    cliente: inputs[0].value,
    monto: inputs[1].value,
    tasa_interes: inputs[2].value,
    plazo: inputs[3].value,
    fecha_otorgamiento: inputs[4].value,
  };

  fetch(`/api/editcredit/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedData),
  })
    .then((response) => {
      if (response.ok) {
        toggleEdit(row, false);
        location.reload(); // Recargar la página para mostrar los cambios
      } else {
        alert("Error al actualizar crédito");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Borrar Credito

function deleteCredit(id) {
  if (!confirm("¿Seguro que deseas eliminar este crédito?")) return;

  fetch(`/api/deletecredit/${id}`, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        location.reload(); // Recargar la página después de eliminar
      } else {
        alert("Error al eliminar crédito");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Código para grafica de creditos otorgados 

document.addEventListener("DOMContentLoaded", function () {
  fetch("api/creditlist")
  .then(response => response.json())
        .then(data => {
            const totalCreditos = data.length;

            new Chart("credito_otorgado", {
                type: "bar",
                data: {
                    labels: ["Créditos otorgados"],
                    datasets: [{
                        backgroundColor: ["orange"],
                        data: [totalCreditos]
                    }]
                },
                options: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Cantidad Total de Créditos Otorgados"
                    }
                }
            });
        })
        .catch(error => console.error("Error al cargar la gráfica:", error));
});

// Grafica relacion cliente - monto 
document.addEventListener("DOMContentLoaded", function () {
  fetch("api/creditlist")
  .then(response => response.json())
        .then(data => {
          let clientes = data.map(credito => credito.cliente);
          let creditos = data.map(credito => credito.monto); 

          let ctxPie = document.getElementById("cliente_monto").getContext("2d");
            new Chart(ctxPie, {
                type: "doughnut",
                data: {
                    labels: clientes,
                    datasets: [{
                        label: "Monto por Cliente",
                        backgroundColor: ["red", "green", "blue", "orange", "purple","brown"],
                        data: creditos
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                      display: true,
                      text: "Relación Monto - Cliente"
                    }
                }
            });
        })
        .catch(error => console.error("Error al cargar la gráfica:", error));
});