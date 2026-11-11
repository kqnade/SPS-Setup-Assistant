using System;
using LumaKroma.Sps2SetupAssistant.Editor.Compatibility;
using NUnit.Framework;
using VRC.SDK3.Avatars.ScriptableObjects;

namespace LumaKroma.Sps2SetupAssistant.Editor.Tests
{
    public class Sps3MenuCompatibilityTests
    {
        private static VRCExpressionsMenu.Control Toggle(string name) =>
            new VRCExpressionsMenu.Control { name = name, type = VRCExpressionsMenu.Control.ControlType.Toggle };

        [TestCase("<b>Auto Mode</b>\n<size=20>Activates hole nearest to a VRCFury plug", false)]
        [TestCase("<b>Auto</b>", false)]
        [TestCase("<b>Legacy Compatibility</b>\n<size=20>DPS / TPS / SPS1\nOne socket at a time", true)]
        [TestCase("<b>Legacy Support</b>\n<size=20>DPS/TPS/SPS1/SPS2\nOne socket at a time", true)]
        public void RecognizesObservedNativeLabels(string label, bool legacy)
        {
            var expected = Toggle(label);
            var found = Sps2BuildIntegration.FindUniqueToggle(new[] { Toggle("Unrelated"), expected },
                legacy ? Sps2BuildIntegration.LegacyLabel : Sps2BuildIntegration.AutoLabel, true,
                legacy ? Sps2BuildIntegration.LegacySps3Label : Sps2BuildIntegration.AutoSps3Label);
            Assert.That(found, Is.SameAs(expected));
            Assert.That(found.name, Is.EqualTo(label), "Recognition must not mutate native controls.");
        }

        [TestCase(false)]
        [TestCase(true)]
        public void OldAndNewControlsTogetherAreRejected(bool legacy)
        {
            string oldLabel = legacy ? Sps2BuildIntegration.LegacyLabel : Sps2BuildIntegration.AutoLabel;
            string newLabel = legacy ? Sps2BuildIntegration.LegacySps3Label : Sps2BuildIntegration.AutoSps3Label;
            Assert.Throws<InvalidOperationException>(() => Sps2BuildIntegration.FindUniqueToggle(
                new[] { Toggle(oldLabel), Toggle(newLabel) }, oldLabel, false, newLabel));
        }

        [Test]
        public void DuplicateNewControlsAreRejected()
        {
            Assert.Throws<InvalidOperationException>(() => Sps2BuildIntegration.FindUniqueToggle(
                new[] { Toggle(Sps2BuildIntegration.LegacySps3Label), Toggle(Sps2BuildIntegration.LegacySps3Label) },
                Sps2BuildIntegration.LegacyLabel, false, Sps2BuildIntegration.LegacySps3Label));
        }

        [Test]
        public void UnknownLabelsAndNonTogglesDoNotMatch()
        {
            var controls = new[] {
                Toggle("Legacy Support"),
                Toggle(Sps2BuildIntegration.LegacySps3Label + " extra"),
                new VRCExpressionsMenu.Control { name = Sps2BuildIntegration.LegacySps3Label,
                    type = VRCExpressionsMenu.Control.ControlType.Button }
            };
            Assert.That(Sps2BuildIntegration.FindUniqueToggle(controls,
                Sps2BuildIntegration.LegacyLabel, false, Sps2BuildIntegration.LegacySps3Label), Is.Null);
            Assert.Throws<InvalidOperationException>(() => Sps2BuildIntegration.FindUniqueToggle(controls,
                Sps2BuildIntegration.LegacyLabel, true, Sps2BuildIntegration.LegacySps3Label));
        }

        [Test]
        public void SocketBuildTokensStillRequireAnExactUniqueMatch()
        {
            const string token = "__SPS2_test_mouth";
            var expected = Toggle(token);
            Assert.That(Sps2BuildIntegration.FindUniqueToggle(new[] { expected }, token, true), Is.SameAs(expected));
            Assert.Throws<InvalidOperationException>(() => Sps2BuildIntegration.FindUniqueToggle(
                new[] { Toggle(token + "_other") }, token, true));
            Assert.Throws<InvalidOperationException>(() => Sps2BuildIntegration.FindUniqueToggle(
                new[] { expected, Toggle(token) }, token, true));
        }
    }
}
