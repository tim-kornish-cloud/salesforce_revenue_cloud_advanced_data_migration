trigger QuoteToContractRCATrigger on Quote (after update) {
    if (Trigger.isAfter && Trigger.isUpdate) {
        QuoteToContractRCATriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
    }
}
