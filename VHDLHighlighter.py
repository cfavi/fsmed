from PyQt4 import QtCore, QtGui


class VHDLHighlighter(QtGui.QSyntaxHighlighter):
    ''' Very basic VHDL syntax highlighter'''
    def __init__(self, parent=None):
        super(VHDLHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywordPatterns = ["\\babs\\b", "\\baccess\\b", "\\bafter\\b",
                           "\\balias\\b", "\\ball\\b", "\\band\\b", "\\barchitecture\\b",
                           "\\barray\\b", "\\bassert\\b", "\\battribute\\b", "\\bbegin\\b",
                           "\\bblock\\b", "\\bbody\\b", "\\bbuffer\\b", "\\bbus\\b",
                           "\\bcase\\b", "\\bcomponent\\b", "\\bconfiguration\\b",
                           "\\bconstant\\b", "\\bdisconnect\\b", "\\bdownto\\b", "\\belse\\b",
                           "\\belsif\\b", "\\bend\\b", "\\bentity\\b", "\\bexit\\b",
                           "\\bfile\\b", "\\bfor\\b", "\\bfunction\\b", "\\bgenerate\\b",
                           "\\bgeneric\\b", "\\bgroup\\b", "\\bguarded\\b", "\\bif\\b",
                           "\\bimpure\\b", "\\bin\\b", "\\binertial\\b", "\\binout\\b",
                           "\\bis\\b", "\\blabel\\b", "\\blibrary\\b", "\\blinkage\\b",
                           "\\bliteral\\b", "\\bloop\\b", "\\bmap\\b", "\\bmod\\b",
                           "\\bnand\\b", "\\bnew\\b", "\\bnext\\b", "\\bnor\\b", "\\bnot\\b",
                           "\\bnull\\b", "\\bof\\b", "\\bon\\b", "\\bopen\\b", "\\bor\\b",
                           "\\bothers\\b", "\\bout\\b", "\\bpackage\\b", "\\bport\\b",
                           "\\bpostponed\\b", "\\bprocedure\\b", "\\bprocess\\b", "\\bpure\\b",
                           "\\brange\\b", "\\brecord\\b", "\\bregister\\b", "\\breject\\b",
                           "\\brem\\b", "\\breport\\b", "\\breturn\\b", "\\brol\\b",
                           "\\bror\\b", "\\bselect\\b", "\\bseverity\\b", "\\bsignal\\b",
                           "\\bshared\\b", "\\bsla\\b", "\\bsll\\b", "\\bsra\\b", "\\bsrl\\b",
                           "\\bsubtype\\b", "\\bthen\\b", "\\bto\\b", "\\btransport\\b",
                           "\\btype\\b", "\\bunaffected\\b", "\\bunits\\b", "\\buntil\\b",
                           "\\buse\\b", "\\bvariable\\b", "\\bwait\\b", "\\bwhen\\b",
                           "\\bwhile\\b", "\\bwith\\b", "\\bxnor\\b", "\\bxor\\b"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)
        singleLineCommentFormat.setFontItalic(True)
        self.highlightingRules.append((QtCore.QRegExp("--[^\n]*"),
                singleLineCommentFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkRed)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                                       quotationFormat))
        self.highlightingRules.append((QtCore.QRegExp("\'.*\'"),
                                       quotationFormat))


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)




