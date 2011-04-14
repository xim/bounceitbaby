[top]
components : C_1@CollaborationManager
in : speed_in
in : help_request_in
in : help_accepted_in
in : help_in
in : help_end_in
out : adjust_speed_out
out : help_out
out : help_end_out
out : help_accepted_out
Link : help_in help_in@C_1
Link : help_end_in help_end_in@C_1
Link : speed_in speed_in@C_1
Link : help_request_in help_request_in@C_1
Link : help_accepted_in help_accepted_in@C_1
Link : help_out@C_1 help_out
Link : help_end_out@C_1 help_end_out
Link : adjust_speed_out@C_1 adjust_speed_out
Link : help_accepted_out@C_1 help_accepted_out

[C_1]
id : 1
maxHelpDuration : 01:00:00:000
speedIncrement : 150
speedDecrement : 50
helpOthersSpeedThreshold : 12
needHelpSpeedThreshold : 7
delayBeforeHelpingAnotherOne : 00:30:00:000
in : help_in
in : speed_in
in : help_end_in
in : help_request_in
in : help_accepted_in
out : adjust_speed_out
out : help_out
out : help_end_out
out : help_accepted_out
