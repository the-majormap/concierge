export default function () {
  const $userType = document.querySelector('#userType');
  return $userType !== null && $userType instanceof HTMLInputElement ? $userType.value : '';
};
