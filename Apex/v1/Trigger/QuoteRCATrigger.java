trigger QuoteRCATrigger on Quote (after update) {
    if (Trigger.isAfter && Trigger.isUpdate) {
        QuoteRCATriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
    }
}
