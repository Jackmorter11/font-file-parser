
class Glyph:
    def __init__(self, coordsX, coordsY, endPtsOfContours):
        # Create list of form [(x, y), (x, y)...]
        self.coordinates = list(zip(coordsX, coordsY))
        self.endPtsOfContours = endPtsOfContours

    def __str__(self):
        """
        Format for glyph points that can be copied into desmos to see shape
        """
        stringFormat = ""

        startPoint = 0
        for endPoint in self.endPtsOfContours:
            segment = self.coordinates[startPoint:endPoint+1]  # Last endPoint to next
            segment.append(self.coordinates[startPoint])       # Repeat the first point to close shape
            stringFormat += str(segment) + "\n"                # Sperate with newline
            startPoint = endPoint+1
        
        return stringFormat