Attribute VB_Name = "ReorderSettings"
Option Compare Database
Option Explicit

' Reorder settings per item. Table: tblReorder(ItemNo, MinQty, ReorderQty, Supplier)

Public Sub ShowReorder(ByVal itemNo As String)
    Dim rs As DAO.Recordset
    Set rs = CurrentDb.OpenRecordset( _
        "SELECT * FROM tblReorder WHERE ItemNo = '" & itemNo & "'")
    If rs.EOF Then
        MsgBox "Item not found"
    Else
        MsgBox rs!ItemNo & ": min " & rs!MinQty & ", reorder " & rs!ReorderQty & ", " & rs!Supplier
    End If
    rs.Close
End Sub

Public Sub SaveReorder(ByVal itemNo As String, ByVal minQty As Long, _
                       ByVal reorderQty As Long, ByVal supplier As String)
    Dim db As DAO.Database
    Set db = CurrentDb
    db.Execute "DELETE FROM tblReorder WHERE ItemNo = '" & itemNo & "'"
    db.Execute "INSERT INTO tblReorder (ItemNo, MinQty, ReorderQty, Supplier) VALUES ('" & _
        itemNo & "', " & minQty & ", " & reorderQty & ", '" & supplier & "')"
End Sub
