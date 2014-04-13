Report Results
==============

### 3.2	TF-IDF
	>> apache
	document id                                       score
	Apache_Isis                                       0.232290
	Southern_Apache_Museum                            0.216969
	Apache_Excalibur                                  0.206819
	Apache_Rocks_the_Bottom!                          0.199597
	Apache_Incubator                                  0.195659
	Fort_Apache                                       0.193399
	Apache_Directory                                  0.189683
	Apache_Forrest                                    0.188877
	Western_Apache_language                           0.187994
	Plains_Apache_language                            0.186527

	>> apache aries
	document id                                       score
	Aries                                             0.278531
	Apache_Aries                                      0.250711
	Apache_Isis                                       0.232290
	Southern_Apache_Museum                            0.216969
	Apache_Excalibur                                  0.206819
	Apache_Rocks_the_Bottom!                          0.199597
	Apache_Incubator                                  0.195659
	Fort_Apache                                       0.193399
	Apache_Directory                                  0.189683
	Apache_Forrest                                    0.188877

	>> apache apache aries
	document id                                       score
	Apache_Isis                                       0.368171
	Southern_Apache_Museum                            0.343888
	Apache_Excalibur                                  0.327800
	Apache_Rocks_the_Bottom!                          0.316355
	Apache_Aries                                      0.313229
	Apache_Incubator                                  0.310112
	Fort_Apache                                       0.306531
	Aries                                             0.304566
	Apache_Directory                                  0.300640
	Apache_Forrest                                    0.299363

### 3.3	Pivoted Length Normalization
	>> apache
	document id                                       score
	Apache_(disambiguation)                           0.157835
	Apache_Rocks_the_Bottom!                          0.152856
	Mod_proxy                                         0.151663
	Western_Apache_language                           0.145874
	Apache_Trail                                      0.143866
	Plains_Apache_language                            0.141442
	Mod_ssl                                           0.140792
	Fort_Apache_Indian_Reservation                    0.139391
	Apache_TomEE                                      0.136530
	Fort_Apache                                       0.135704

	>> apache aries
	document id                                       score
	Aries                                             0.220485
	Apache_ServiceMix                                 0.165268
	Apache_(disambiguation)                           0.157835
	Aries_Marine                                      0.157389
	Aries_(comics)                                    0.153568
	Apache_Rocks_the_Bottom!                          0.152856
	Mod_proxy                                         0.151663
	Apache_Aries                                      0.151362
	USS_Aries_(PHM-5)                                 0.148377
	OSGi_Specification_Implementations                0.147210

	>> apache apache aries
	document id                                       score
	Apache_(disambiguation)                           0.250162
	Apache_Rocks_the_Bottom!                          0.242271
	Aries                                             0.241095
	Mod_proxy                                         0.240380
	Apache_ServiceMix                                 0.237173
	Western_Apache_language                           0.231205
	Apache_Trail                                      0.228023
	Plains_Apache_language                            0.224180
	Mod_ssl                                           0.223150
	Fort_Apache_Indian_Reservation                    0.220929

### 3.4
#### Without Requiring All Query Terms
	>> apache james
	document id                                       score
	James                                             0.185760
	Apache_James                                      0.171157
	Apache_(disambiguation)                           0.157835
	Apache_Rocks_the_Bottom!                          0.152856
	Mod_proxy                                         0.151663
	Battle_of_Fort_Apache                             0.146745
	Western_Apache_language                           0.145874
	Apache_Trail                                      0.143866
	Plains_Apache_language                            0.141442
	Mod_ssl                                           0.140792

	>> apache forrest
	document id                                       score
	Forrest                                           0.269122
	Forrest_(surname)                                 0.226635
	Apache_Forrest                                    0.218972
	John_Forrest_(disambiguation)                     0.207705
	Forrest_(given_name)                              0.202369
	James_Forrest                                     0.189919
	George_Forrest                                    0.184893
	Forrest_Gump_–_Original_Motion_Picture_Score      0.173833
	David_Forrest_(Australian_politician)             0.171349
	Forrest,_Manitoba                                 0.167464

	>> apache aries
	document id                                       score
	Aries                                             0.220485
	Apache_ServiceMix                                 0.165268
	Apache_(disambiguation)                           0.157835
	Aries_Marine                                      0.157389
	Aries_(comics)                                    0.153568
	Apache_Rocks_the_Bottom!                          0.152856
	Mod_proxy                                         0.151663
	Apache_Aries                                      0.151362
	USS_Aries_(PHM-5)                                 0.148377
	OSGi_Specification_Implementations                0.147210


#### Requiring All Query Terms
	>> apache james
	document id                                       score
	James                                             0.185760
	Apache_James                                      0.171157
	Battle_of_Fort_Apache                             0.146745
	James_Kirker                                      0.139125
	Mari_Apache                                       0.135101
	James_H._Turpin                                   0.134121
	Apache–Mexico_Wars                                0.131857
	Apache_Wars                                       0.131042
	Apache_Kid                                        0.128378
	James_B._Gillett                                  0.124260

	>> apache forrest
	document id                                       score
	Forrest                                           0.269122
	Apache_Forrest                                    0.218972
	Apache_Kid                                        0.141312
	Gump                                              0.137806
	Apache_XML                                        0.125621
	Geronimo                                          0.106817
	List_of_Apache_Software_Foundation_projects       0.106125
	Apache_Ambush                                     0.093786
	List_of_places_in_Arizona_(A–G)                   0.084701
	The_Adventures_of_Rin_Tin_Tin                     0.080854

	>> apache aries
	document id                                       score
	Aries                                             0.220485
	Apache_ServiceMix                                 0.165268
	Apache_Aries                                      0.151362
	OSGi_Specification_Implementations                0.147210
	Apache_Felix                                      0.128895
	List_of_rockets_launched_from_Esrange             0.099404
	Write-ahead_logging                               0.082353
	OSGi                                              0.069220
	Link_16                                           0.053584

### 3.6 Implementing Disambiguation

Parameters used: alpha=1, beta=0.5, gamma=100, k=100

	>> abdera
	document id                                       score
	Apache_Abdera                                     1.500847
	Abdera,_Thrace                                    1.110492
	Acraea_abdera                                     1.042033
	Abderites                                         0.808831
	List_of_Apache_Software_Foundation_projects       0.761438
	Hecataeus_of_Abdera                               0.684331
	Archaeological_Museum_of_Abdera                   0.644658
	Xanthi_(regional_unit)                            0.618798
	List_of_Thracian_Greeks                           0.606558
	Polystylus_(place)                                0.579369

	>> aries
	document id                                       score
	OSGi                                              0.443121
	Sacrifice_(2012)                                  0.410796
	OSGi_Specification_Implementations                0.346124
	Apache_Aries                                      0.299693
	Apache_Felix                                      0.261520
	Wolseley_Aries                                    0.231954
	Circus_(company)                                  0.228342
	Invisible_Hands_Music                             0.220974
	The_Age_of_the_Fall                               0.220564
	Plymouth_Reliant                                  0.220331

	>> beehive
	document id                                       score
	List_of_Apache_Software_Foundation_projects       0.759545
	Content_repository_API_for_Java                   0.479098
	Apache_Attic                                      0.473162
	Voice_of_the_Beehive                              0.368938
	Best_Of_(Voice_of_the_Beehive_album)              0.362363
	Young_Women_(organization)                        0.360362
	A_Portrait                                        0.332407
	Content_(album)                                   0.329652
	Now_That's_What_I_Call_Music!_15_(South_African_series)0.322098
	Gateway_Playhouse                                 0.310858

	>> click
	document id                                       score
	Java_view_technologies_and_frameworks             0.572800
	You_&_I_(Graham_Coxon_song)                       0.405272
	Van_Jones                                         0.395310
	Empty_(The_Click_Five_song)                       0.363398
	Triple-click                                      0.356648
	Click_chemistry                                   0.352399
	Bonnie_Dundee                                     0.347001
	Cross-site_request_forgery                        0.346841
	Click.to                                          0.343360
	Dental_clicks                                     0.333935

	>> forrest
	document id                                       score
	List_of_Apache_Software_Foundation_projects       0.758514
	Apache_XML                                        0.576721
	Forrest_Gump_–_Original_Motion_Picture_Score      0.485766
	Nathan_Bedford_Forrest                            0.474126
	List_of_number-one_albums_in_Australia_during_the_1990s0.370311
	Forrest_Gump_(character)                          0.349668
	Bell_Ord_Forrest                                  0.343638
	Katherine_B._Forrest                              0.340951
	Geronimo                                          0.333371
	Down_the_Hillside                                 0.305696

	>> james
	document id                                       score
	Atom_(standard)                                   1.137192
	List_of_Apache_Software_Foundation_projects       0.744822
	StAX                                              0.637201
	How_Opal_Mehta_Got_Kissed,_Got_Wild,_and_Got_a_Life0.628145
	Apache_Ant                                        0.601660
	Phil_Keaggy                                       0.537742
	Java_Servlet                                      0.532548
	Groovy_(programming_language)                     0.529769
	Sexy_to_Me                                        0.479794
	Comparison_of_C_Sharp_and_Java                    0.460035

	>> shale
	document id                                       score
	List_of_Apache_Software_Foundation_projects       0.759667
	Shale_oil_extraction                              0.315972
	Alberta_Taciuk_process                            0.315051
	Shale_oil                                         0.269449
	Petrosix                                          0.264012
	Ambre_Energy                                      0.261122
	Oil_shale_in_Jordan                               0.257075
	History_of_the_oil_shale_industry                 0.255882
	Oil_shale                                         0.250792
	Oil_shale_industry                                0.248646

	>> sling
	document id                                       score
	Comparison_of_server-side_JavaScript_solutions    0.557017
	Apache_Sling                                      0.511896
	Birmingham_(Live_with_Orchestra_&_Choir)          0.467976
	OSGi                                              0.442783
	On_the_Verge_of_Something_Wonderful               0.355571
	The_Curse_of_Singapore_Sling                      0.351570
	Singapore_Sling_(band)                            0.339188
	Day_Software                                      0.330932
	Hook_N_Sling                                      0.329103
	Jefferson_Mays                                    0.324213

	>> synapse
	document id                                       score
	Synapse_Films                                     0.425251
	Apache_Synapse                                    0.356369
	Enterprise_service_bus                            0.293057
	Enterprise_application_integration                0.291903
	Golgi_cell                                        0.286945
	Synapse_Group,_Inc.                               0.279370
	WSO2                                              0.278272
	Heaven's_Lost_Property                            0.276999
	Peltarion_Synapse                                 0.273922
	Squid_giant_synapse                               0.269802

	>> tiles
	document id                                       score
	Vroom_Framework                                   0.657222
	Java_view_technologies_and_frameworks             0.612161
	Spring_Roo                                        0.446647
	Development_of_Windows_Vista                      0.355038
	List_of_songs_recorded_by_Led_Zeppelin            0.305540
	Apache_Struts                                     0.298678
	Led_Zeppelin_Japanese_Tour_1971                   0.270542
	Justin_Duerr                                      0.196679
	National_Museum_of_Singapore                      0.191650
	Rasdaman                                          0.191271

	>> tuscany
	document id                                       score
	List_of_Apache_Software_Foundation_projects       0.759761
	History_of_Tuscany                                0.324360
	Apache_Tuscany                                    0.319926
	Princess_Maria_Antonia_of_the_Two_Sicilies        0.315628
	List_of_rulers_of_Tuscany                         0.292969
	Duke_of_Spoleto                                   0.292485
	Grand_Princes_of_Tuscany                          0.288254
	Service_Component_Architecture                    0.282898
	Cosimo                                            0.273523
	Java_API_for_RESTful_Web_Services                 0.262446

	>> request
	document id                                       score
	Representational_state_transfer                   0.838163
	JSONP                                             0.835743
	JSON-RPC                                          0.771129
	XML_Interface_for_Network_Services                0.711109
	XMLHttpRequest                                    0.696160
	XML-Retrieval                                     0.679174
	Vroom_Framework                                   0.675166
	Json2Ldap                                         0.662614
	AJAJ                                              0.651399
	Security_Assertion_Markup_Language                0.621371

	>> message
	document id                                       score
	Representational_state_transfer                   0.820764
	List_of_Apache_Software_Foundation_projects       0.774405
	JSON-RPC                                          0.752292
	Internet_media_type                               0.723632
	Json2Ldap                                         0.664496
	Push_Access_Protocol                              0.635212
	AJAJ                                              0.634385
	SAML_1.1                                          0.608398
	Security_Assertion_Markup_Language                0.600665
	Enterprise_JavaBeans                              0.590460

	>> user
	document id                                       score
	Representational_state_transfer                   0.825995
	JSONP                                             0.765189
	JSON-RPC                                          0.727650
	Internet_media_type                               0.689434
	XMLHttpRequest                                    0.671786
	Vroom_Framework                                   0.665445
	StAX                                              0.652737
	Apache_Maven                                      0.618328
	AJAJ                                              0.615369
	Security_Assertion_Markup_Language                0.614132

	>> file
	document id                                       score
	Internationalization_Tag_Set                      0.779087
	JSONP                                             0.766063
	Canonicalization                                  0.741302
	Internet_media_type                               0.722039
	XML_Interface_for_Network_Services                0.709990
	Vroom_Framework                                   0.695500
	JAR_(file_format)                                 0.660545
	Java_API_for_XML_Processing                       0.653362
	Apache_Ant                                        0.652324
	Apache_Maven                                      0.643215

	>> service
	document id                                       score
	Representational_state_transfer                   0.820470
	JSONP                                             0.766758
	List_of_Apache_Software_Foundation_projects       0.764043
	JSON-RPC                                          0.746560
	XML_Interface_for_Network_Services                0.701351
	Sam_Ruby                                          0.648556
	Json2Ldap                                         0.637681
	SAML_1.1                                          0.608603
	Security_Assertion_Markup_Language                0.603404
	Java_Community_Process                            0.585931

	>> class
	document id                                       score
	Internationalization_Tag_Set                      0.749523
	JSON-RPC                                          0.731406
	Vroom_Framework                                   0.683521
	Java_API_for_XML_Processing                       0.671956
	StAX                                              0.636983
	How_Opal_Mehta_Got_Kissed,_Got_Wild,_and_Got_a_Life0.632757
	Apache_Maven                                      0.605594
	XMLBeans                                          0.600324
	JAR_(file_format)                                 0.598340
	Gotcha_(programming)                              0.589756

	>> file request
	document id                                       score
	JSONP                                             0.855560
	Vroom_Framework                                   0.741398
	XML_Interface_for_Network_Services                0.736010
	JAR_(file_format)                                 0.681014
	Java_Servlet                                      0.649075
	X_Window_System_core_protocol                     0.631823
	Hypertext_Transfer_Protocol                       0.629215
	List_of_HTTP_status_codes                         0.625680
	List_of_HTTP_header_fields                        0.597670
	URL_redirection                                   0.591034
