import maya.api.OpenMaya as om


def _itermaya(obj, accessor):
    while not obj.isDone():
        yield accessor()
        obj.next()


def tomaya(obj, getter='getDependNode'):
    msel = om.MSelectionList()
    msel.add(obj)
    it = om.MItSelectionList(msel)
    for obj in _itermaya(it, getattr(it, getter)):
        yield obj


def idag(root=None, getter='currentItem', traversal=om.MItDag.kDepthFirst, filtertype=om.MFn.kInvalid):
    it = om.MItDag()
    it.reset(root or it.root(), traversal, filtertype)
    for obj in _itermaya(it, getattr(it, getter)):
        yield obj


def idg(root, getter='currentNode', traversal=om.MItDependencyGraph.kDepthFirst, filtertype=om.MFn.kInvalid,
        direction=om.MItDependencyGraph.kDownstream, level=om.MItDependencyGraph.kNodeLevel):
    it = om.MItDependencyGraph(root)
    it.resetTo(root, filtertype, direction, traversal, level)
    for obj in _itermaya(it, getattr(it, getter)):
        yield obj


__all__ = ['tomaya', 'idag', 'idg']
