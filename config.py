
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
		testGlobalConfiguration["GREEN_LOWER"] = (20, 20, 50)
		testGlobalConfiguration["GREEN_UPPER"] = (100, 100, 250)
		testGlobalConfiguration["CYAN_LOWER"] = (35, 60, 150)
		testGlobalConfiguration["CYAN_UPPER"] = (150, 255, 255)
		testGlobalConfiguration["RED_LOWER"] = (100, 170, 200)
		testGlobalConfiguration["RED_UPPER"] = (220, 255, 255)
		testGlobalConfiguration["GREENPURE_LOWER"] = (15, 100, 202)
		testGlobalConfiguration["GREENPURE_UPPER"] = (130, 127, 250)
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
