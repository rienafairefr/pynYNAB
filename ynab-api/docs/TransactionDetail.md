# TransactionDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**date** | **date** |  | 
**amount** | **float** | The transaction amount in milliunits format | 
**cleared** | **str** | The cleared status of the transaction | 
**approved** | **bool** | Whether or not the transaction is approved | 
**account_id** | **str** |  | 
**subtransactions** | [**list[SubTransaction]**](SubTransaction.md) | If a split transaction, the sub-transactions. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


