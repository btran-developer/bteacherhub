const teacherNameField = $("select[name='teacher']");
const fromDateField = $("input[name='from_date']");
const toDateField = $("input[name='to_date']");
const summarySection = $(
  "<div class='card py-2 px-3 my-3' style='width: 18rem'><div class='card-body'><p class='card-text'></p></div><div>"
);
const reportsListContainer = $("#report-list-container");
const reportsList = $("#report-list");
const loadMoreButton = $("#load-more-btn");
const spinner = $(".spinner-border");
const deleteReportsConfirmationModal = $("#deleteReportsModal");

let next_page = "";

reportsListContainer.hide();
loadMoreButton.hide();
spinner.hide();

$("input[value='Get']").on("click", e => {
  e.preventDefault();

  $.ajax({
    url: $SCRIPT_ROOT + "/report",
    method: "GET",
    data: {
      teacher: teacherNameField.val(),
      from_date: fromDateField.val(),
      to_date: toDateField.val()
    }
  })
    .done(data => {
      if (data["number_of_errors"] > 0) {
        if (data["errors"]["teacher_errors"].length > 0) {
          let error = data["errors"]["teacher_errors"][0];

          teacherNameField.addClass("is-invalid");
          $(".teacher-error").text(error);
        } else {
          teacherNameField.removeClass("is-invalid");
        }

        if (data["errors"]["from_date_errors"].length > 0) {
          let error = data["errors"]["from_date_errors"][0];

          fromDateField.addClass("is-invalid");
          $(".from-date-error").text(error);
        } else {
          fromDateField.removeClass("is-invalid");
        }

        if (data["errors"]["to_date_errors"].length > 0) {
          let error = data["errors"]["to_date_errors"][0];

          toDateField.addClass("is-invalid");
          $(".to-date-error").text(error);
        } else {
          toDateField.removeClass("is-invalid");
        }
      } else {
        teacherNameField.removeClass("is-invalid");
        fromDateField.removeClass("is-invalid");
        toDateField.removeClass("is-invalid");
        summarySection.empty();

        if (data["data"]["search_type"] !== "ALL") {
          let teacherAttendance = $(
            `<div><strong>Teacher attendance</strong>:&nbsp;<span>${data["data"]["teacher_attendance"]}</span></div>`
          );

          let asMainTeacher = $(
            `<div><strong>Day as main teacher</strong>:&nbsp;<span>${data["data"]["day_as_main"]}</span></div>`
          );

          let asAssistantTeacher = $(
            `<div><strong>Day as assistant teacher</strong>:&nbsp;<span>${data["data"]["day_as_assistant"]}</span></div>`
          );

          summarySection.append(teacherAttendance);
          summarySection.append(asMainTeacher);
          summarySection.append(asAssistantTeacher);
        } else {
          let totalReports = $(
            `<div><strong>Total Reports</strong>:&nbsp;<span>${data["data"]["total_reports"]}</span></div>`
          );

          let exportToCsvButton = $(
            `<a class='btn btn-success' href='/report/get-csv?from_date=${fromDateField.val()}&to_date=${toDateField.val()}'>Export to CSV</a>`
          );

          let deleteFoundReportsButton = $(
            "<button class='btn btn-danger'>Delete found reports</button>"
          );

          deleteFoundReportsButton.on("click", e => {
            deleteReportsConfirmationModal.modal("show");
            deleteReportsConfirmationModal
              .find(".modal-body")
              .text(
                `Are you sure you want to delete reports from ${fromDateField.val()} to ${toDateField.val()}`
              );
          });

          let buttonGroup = $(
            "<div class='btn-group btn-group-sm' role='group' aria-label='reports actions'></div>"
          );

          buttonGroup.append(exportToCsvButton);
          buttonGroup.append(deleteFoundReportsButton);

          summarySection.append(totalReports);
          summarySection.append(buttonGroup);
        }

        $("form").after(summarySection);

        reportsListContainer.show();

        next_page = data["next_page_num"];

        if (data["next_page_num"]) {
          loadMoreButton.show();
        }

        reportsList.empty();
        loadReportToList(data["data"]["reports"]);
      }
    })
    .fail((jqXHR, textStatus, errorThrown) => {
      alert(`${errorThrown}! Please check back later.`);
    });
});

loadMoreButton.on("click", e => {
  e.stopPropagation();

  loadMoreButton.hide();
  spinner.show();

  $.ajax({
    url: $SCRIPT_ROOT + "/report",
    method: "GET",
    data: {
      teacher: teacherNameField.val(),
      from_date: fromDateField.val(),
      to_date: toDateField.val(),
      page: next_page
    }
  }).done(data => {
    next_page = data["next_page_num"];

    if (data["next_page_num"]) {
      loadMoreButton.show();
    } else {
      loadMoreButton.hide();
    }

    spinner.hide();

    loadReportToList(data.data.reports);
  });
});

$("#deleteReports").on("click", function(e) {
  $(this).text("");
  $(this).append(
    $(
      "<div class='spinner-border spinner-border-sm' role='status'><span class='sr-only'>Loading...</span></div>"
    )
  );
  $.ajax({
    url: $SCRIPT_ROOT + "/report/delete",
    method: "GET",
    data: {
      from_date: fromDateField.val(),
      to_date: toDateField.val()
    }
  }).done((data, textStatus) => {
    if (textStatus === "success") {
      alert(data.message);
      window.location.href = "/report";
    } else {
      alert(data.message);
    }
  });
});

const loadReportToList = reports => {
  reports.forEach(report => {
    let date = new Date(report["teaching_date"]);
    let { id, main_teacher, assistant_teacher, submitted_by } = report;
    let dateString = `${date.getDate()}/${date.getMonth() +
      1}/${date.getFullYear()}`;
    let reportItem = $(
      `<a href="/report/${id}" class="list-group-item list-group-item-action"></a>`
    );

    let reportItemHeader = $(
      '<div class="d-flex w-100 justify-content-between"></div>'
    );

    reportItemHeader.append($(`<h5 class="mb-1">${dateString}</h5>`));

    reportItemHeader.append(
      $(`<small>Submitted by: ${submitted_by.teacher_name || "n/a"}</small>`)
    );

    reportItem.append(reportItemHeader);

    reportItem.append(
      $(
        `<p class="mb-1"><strong>Main teacher:</strong>&nbsp;${main_teacher.teacher_name}</p>`
      )
    );
    reportItem.append(
      $(
        `<p class="mb-1"><strong>Assitant:</strong>&nbsp;${assistant_teacher.teacher_name ||
          "n/a"}</p>`
      )
    );

    reportsList.append(reportItem);
  });
};
