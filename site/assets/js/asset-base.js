(function () {
    const path = window.location.pathname.replace(/\\/g, '/');
    if (path === '/Git-Workflow-Lab' || path.startsWith('/Git-Workflow-Lab/')) {
        const base = document.createElement('base');
        base.href = '/Git-Workflow-Lab/';
        document.head.prepend(base);
    }
})();
