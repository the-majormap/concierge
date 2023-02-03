/*
 *  https://junilhwang.github.io/TIL/Javascript/Design/Vanilla-JS-Component/
 *
 */
function updateElement(parent, newNode, oldNode) {
  if (!newNode && oldNode) return oldNode.remove();
  if (newNode && !oldNode) return parent.appendChild(newNode);
  if (newNode instanceof Text && oldNode instanceof Text) {
    if (oldNode.nodeValue === newNode.nodeValue) return;
    oldNode.nodeValue = newNode.nodeValue
    return;
  }
  if (newNode.nodeName !== oldNode.nodeName) {
    const index = [ ...parent.childNodes ].indexOf(oldNode);
    oldNode.remove();
    parent.appendChild(newNode, index);
    return;
  }
  updateAttributes(oldNode, newNode);

  const newChildren = [ ...newNode.childNodes ];
  const oldChildren = [ ...oldNode.childNodes ];
  const maxLength = Math.max(newChildren.length, oldChildren.length);
  for (let i = 0; i < maxLength; i++) {
    updateElement(oldNode, newChildren[i], oldChildren[i]);
  }
}

function updateAttributes(oldNode, newNode) {
  for (const {name, value} of [ ...newNode.attributes ]) {
    if (value === oldNode.getAttribute(name)) continue;
    oldNode.setAttribute(name, value);
  }
  for (const {name} of [ ...oldNode.attributes ]) {
    if (newNode.getAttribute(name) !== undefined) continue;
    oldNode.removeAttribute(name);
  }
}

class Component {
  $element;
  props;
  state;
  constructor($target, props = {}) {
    this.$element = $target;
    this.props = { ...props };
    this.setup();
    this.render();
    this.created();
  }
  setup() {}
  mounted() {}
  created() {}
  template() { return ''; }
  render() {
    const { $element } = this;

    // 기존 Node를 복제한 후에 새로운 템플릿을 채워넣는다.
    const newNode = $element.cloneNode(true);
    newNode.innerHTML = this.template();

    // DIFF알고리즘을 적용한다.
    const oldChildNodes = [ ...$element.childNodes ];
    const newChildNodes = [ ...newNode.childNodes ];
    const max = Math.max(oldChildNodes.length, newChildNodes.length);
    for (let i = 0; i < max; i++) {
      updateElement($element, newChildNodes[i], oldChildNodes[i]);
    }

    this.mounted();

    // 이벤트를 등록한다.
    requestAnimationFrame(() => this.setEvent());
  }
  setEvent() {}
  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.render();
  }
}

export default Component;
