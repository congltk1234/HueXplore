(this.webpackJsonpstreamlit_sortables=this.webpackJsonpstreamlit_sortables||[]).push([[0],{28:function(e,t,n){},30:function(e,t,n){e.exports=n(38)},38:function(e,t,n){"use strict";n.r(t);var r=n(5),a=n.n(r),i=n(18),c=n.n(i),s=n(7),o=n(10),d=n(26),l=n(14),u=n(21),m=n(9),f=(n(28),function(e){var t=Object(u.e)({id:e.id}),n=t.attributes,r=t.listeners,i=t.setNodeRef,c=t.transform,s=t.transition,o={transform:m.a.Transform.toString(c),transition:s},d="btn shadow-none sortable-item "+(e.isActive?"active":"");return a.a.createElement("li",Object.assign({className:d,ref:i,style:o},n,r),e.children?e.children:null)});function v(e){var t=Object(l.m)({id:e.header}).setNodeRef;return a.a.createElement("div",{className:"sortable-container",ref:t,style:{width:e.width}},e.header?a.a.createElement("div",{className:"container-header"},e.header):null,a.a.createElement(u.a,{id:e.header,items:e.items,strategy:u.c},a.a.createElement("div",{className:"container-body"},e.children)))}function b(e){var t=Object(r.useState)(e.items),n=Object(o.a)(t,2),i=n[0],c=n[1],m=Object(r.useState)(e.items),b=Object(o.a)(m,2),h=b[0],O=b[1],j=Object(r.useState)(null),E=Object(o.a)(j,2),g=E[0],p=E[1],y=Object(l.o)(Object(l.n)(l.e,{activationConstraint:{distance:10}}),Object(l.n)(l.f,{activationConstraint:{delay:250,tolerance:5}}),Object(l.n)(l.d,{coordinateGetter:u.d}));return a.a.createElement(l.a,{sensors:y,onDragEnd:function(e){p(null);var t=e.active,n=e.over;if(!n)return;var r=N(t.id),a=N(n.id);if(r===a){var s=i[r],o=s.items.indexOf(t.id),l=s.items.indexOf(n.id),m=i.map((function(e,t){var n=e.header,a=e.items;return t===r?{header:n,items:Object(u.b)(a,o,l)}:{header:n,items:a}}));c(m),function(e,t){if(e.length!==t.length)return!1;return e.every((function(e,n){var r=e.header,a=e.items,i=t[n];return r===i.header&&a.every((function(e,t){return e===i.items[t]}))}))}(h,m)||d.a.setComponentValue(m)}},onDragOver:function(e){var t=e.active,n=e.over;if(!n)return;var r=N(t.id),a=N(n.id);if(a<0)return;if(r===a)return;console.log(t.id,n.id);var o=i[r].items.indexOf(t.id),d=i[r].items[o],l=i.map((function(e,t){var n=e.header,i=e.items;return t===r?{header:n,items:[].concat(Object(s.a)(i.slice(0,o)),Object(s.a)(i.slice(o+1)))}:t===a?{header:n,items:[].concat(Object(s.a)(i.slice(0,o)),[d],Object(s.a)(i.slice(o)))}:{header:n,items:i}}));c(l)},onDragStart:function(e){p(e.active.id),O(i)},onDragCancel:function(){console.log("canceled"),p(null),c(h)}},i.map((function(t){var n=t.header,r=t.items;return a.a.createElement(v,{key:n,header:n,items:r,direction:e.direction},r.map((function(e){return a.a.createElement(f,{key:e,id:e,isActive:e===g},e)})))})),a.a.createElement(l.b,null,a.a.createElement(f,{id:""},g)));function N(e){var t=i.findIndex((function(t){return t.header===e}));return t>=0?t:i.findIndex((function(t){return t.items.includes(e)}))}}var h=Object(d.b)((function(e){var t=e.args,n=t.items,i="sortable-component "+t.direction;return Object(r.useEffect)((function(){return d.a.setFrameHeight()})),a.a.createElement("div",{className:i},a.a.createElement(b,{items:n,direction:t.direction}))}));c.a.render(a.a.createElement(a.a.StrictMode,null,a.a.createElement(h,null)),document.getElementById("root"))}},[[30,1,2]]]);
//# sourceMappingURL=main.cd1fc43e.chunk.js.map