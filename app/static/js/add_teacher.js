if ($(".invalid-feedback").length) {
  $(".teacher-name-error").length
    ? $("input[name='teacher_name']").addClass("is-invalid")
    : null;
}
