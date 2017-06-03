
#TEST_GLOBAL_PARAMETERS_PATH="testGlobalParameters.properties"
#RELEASE_GLOBAL_PARAMETERS="releaseGlobalParameters.properties"

class Config: 

	def createTestGlobalConfiguration():
		
		testGlobalConfiguration=dict()

		#markers (in meters)
		testGlobalConfiguration["MARKERS_WIDTH"] = 32 * 10**(-2) 
		testGlobalConfiguration["MARKERS_HEIGHT"] = 32 * 10**(-2)
		testGlobalConfiguration["SUPPOSED_FPS"] = 30

		#See if useful parameters..
		testGlobalConfiguration["CAMERA_FLOOR_DISTANCE"] = 24
		testGlobalConfiguration["MARKER_Z_LENGTH"] = 3
		testGlobalConfiguration["BALLSIZE"]=7

		#masks
		testGlobalConfiguration["GREEN_LOWER"] = (23, 23, 102)
		testGlobalConfiguration["GREEN_UPPER"] = (100, 100, 250)
		testGlobalConfiguration["CYAN_LOWER"] = (25, 52, 102)
		testGlobalConfiguration["CYAN_UPPER"] = (200, 255, 255)
		testGlobalConfiguration["RED_LOWER"] = (140 , 140 , 140)
		testGlobalConfiguration["RED_UPPER"] = (250, 200 ,200)
		testGlobalConfiguration["GREENPURE_LOWER"] = (17, 17, 40)
		testGlobalConfiguration["GREENPURE_UPPER"] = (180, 255, 200)


		return testGlobalConfiguration

	def createReleaseGlobalConfiguration():
		
		testGlobalConfiguration=dict()

		#markers (in meters)
		testGlobalConfiguration["MARKERS_WIDTH"] = 32 * 10**(-2) 
		testGlobalConfiguration["MARKERS_HEIGHT"] = 32 * 10**(-2)
		testGlobalConfiguration["SUPPOSED_FPS"] = 30

		#masks
		testGlobalConfiguration["GREEN_LOWER"] = (23, 23, 102)
		testGlobalConfiguration["GREEN_UPPER"] = (100, 100, 250)
		testGlobalConfiguration["CYAN_LOWER"] = (23, 50, 100)
		testGlobalConfiguration["CYAN_UPPER"] = (200, 255, 255)

		return testGlobalConfiguration
