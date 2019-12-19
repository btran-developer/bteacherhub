if ($(".invalid-feedback").length) {
  $(".main-teacher-error").length
    ? $("select[name='main_teacher']").addClass("is-invalid")
    : null;
  $(".assistant-teacher-error").length
    ? $("select[name='assistant_teacher']").addClass("is-invalid")
    : null;
  $(".teaching-date-error").length
    ? $("input[name='teaching_date']").addClass("is-invalid")
    : null;
  $(".teaching-content-error").length
    ? $("textarea[name='teaching_content']").addClass("is-invalid")
    : null;
  $(".student-attendance-error").length
    ? $("input[name='student_attendance']").addClass("is-invalid")
    : null;
  $(".submitted-by-error").length
    ? $("select[name='submitted_by']").addClass("is-invalid")
    : null;
}
