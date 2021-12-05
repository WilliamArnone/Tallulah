from DOTParser import DOTParser


def EdgeFromCtx(ctx:DOTParser.Edge_stmtContext):
    start = ctx.children[0].getText().replace('"', "")
    end = ctx.children[1].children[1].getText().replace('"', "")
    label = ctx.children[2].children[1].children[2].getText().replace('"', "")
    return (start, label, end)

def IndipendenceFromCtx(ctx:DOTParser.Indipendence_commentContext):
    start = ctx.children[2].getText()
    label = ctx.children[4].getText()
    end = ctx.children[6].getText()
    first_reverse = ctx.children[0].getText()=='<'
    this_reverse = ctx.children[1].getText()=='<'
    return (first_reverse, (start, label, end, this_reverse))