@IsTest
public class QuoteRCATriggerHandlerTest {

    @IsTest
    static void testQuoteRCATriggerHandler() {
        // Step 2: Prepare test data
        Contact badContact = new Contact(LastName = 'INVALIDNAME');

        // Step 3: Perform DML operation and test execution
        Test.startTest();
        Database.SaveResult result = Database.insert(badContact, false);
        Test.stopTest();

        // Step 4: Verify results using System.Assert
        System.assert(!result.isSuccess(), 'The contact should not be inserted.');
        System.assert(result.getErrors().size() > 0, 'An error should be returned.');
    }
}
