if ($(".invalid-feedback").length) {
  $(".username-error").length
    ? $("input[name='username']").addClass("is-invalid")
    : null;
  $(".password-error").length
    ? $("input[name='password']").addClass("is-invalid")
    : null;
}
