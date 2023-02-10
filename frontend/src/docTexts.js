let docTexts;

docTexts = {
    docText: `
    User guide for the different tabs. 
    `,
    samplesText: `
    The samples tab shows samples ready for interpretation

    In addtition, it is possible to import new samples.

    When a sample is opened, a new window containing its variants is displayed.
    Clincking the info button on any variant will allow editing of that variant.
    If the same variant has been classified before, that previous info will be shown.
    To reclassify a variant, the edit variant button must be clicked. Editing this info will
    change the classification date. Information not related to the classification of the 
    variant can always be edited, and will nto change the classification date. The information which
    can be edited is: reply, alternative annotation, and the sample specific comment.
    ...

    When interpretation is done the sign off button should be clicked. This will send the sample to
    control. Clicking this button is not allowed if any reply fields are missing. To quickly fill replies, the
    'Fill Reply' button can be used. This will set no to the reply field of any variant which does not have a set
    reply. In addition, any such variant will get the Not evaluated class, if no class is already set.
    The failed sample button also sets all replies to no, and sets the state of the sample to 'Failed'. 
    Such samples are not sent to control.

    When a sample is signed off both user and date is stored.
    `,
    controlText: `
    Successful samples that have been signed off at interpretation can be vertified here.

    The control must be done by a different user.

    Any change to the variant information will result in the sample being sent back automatically.

    If everything looks good the sample can be vertified as finished. User and date is noted.
    `,
    allSamplesText: `
    Displays all samples from the past year.

    Allows for lookup of samples based on run ID or sample ID.

    Clicking on a sample will bring up its variants.
    `,
    varStatsText: `
    Allows variant lookup based on different search terms. 

    Shows how many samples the variant has been detected in, which gene panels were used for each 
    sample as well as reply. Variant class is also included.
    `,
    statisticsText: `
    Shows overview statistics of the past year. Also allows for date based lookup.
    
    `,
    reportText: `
    After interpretation and control is done, a report may be generated here based on results.

    Samples shown will be fro mthe most recent run with at least one finished sample.
    Lookup of samples and runs based on ID is also possible.

    Click on a variant and select a response. The response will be fully or partially filled with variant data.
    
    `,

}

export { docTexts };