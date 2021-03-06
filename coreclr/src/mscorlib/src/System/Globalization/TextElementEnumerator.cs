// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.
// See the LICENSE file in the project root for more information.

////////////////////////////////////////////////////////////////////////////
//
//
//  Purpose:  
//
//
////////////////////////////////////////////////////////////////////////////

using System.Collections;
using System.Diagnostics;
using System.Runtime.Serialization;

namespace System.Globalization
{
    //
    // This is public because GetTextElement() is public.
    //

    public class TextElementEnumerator : IEnumerator
    {
        private String _str;
        private int _index;
        private int _startIndex;

        [NonSerialized] 
        private int _strLen;                // This is the length of the total string, counting from the beginning of string.

        [NonSerialized] 
        private int _currTextElementLen; // The current text element lenght after MoveNext() is called.

        [OptionalField(VersionAdded = 2)] 
        private UnicodeCategory _uc;

        [OptionalField(VersionAdded = 2)] 
        private int _charLen;            // The next abstract char to look at after MoveNext() is called.  It could be 1 or 2, depending on if it is a surrogate or not.

        internal TextElementEnumerator(String str, int startIndex, int strLen)
        {
            Debug.Assert(str != null, "TextElementEnumerator(): str != null");
            Debug.Assert(startIndex >= 0 && strLen >= 0, "TextElementEnumerator(): startIndex >= 0 && strLen >= 0");
            Debug.Assert(strLen >= startIndex, "TextElementEnumerator(): strLen >= startIndex");
            _str = str;
            _startIndex = startIndex;
            _strLen = strLen;
            Reset();
        }

        // the following fields is defined to keep the compatibility with Everett.
        // don't change/remove the names/types of these fields.
        private int _endIndex;
        private int _nextTextElementLen;

        [OnDeserializing]
        private void OnDeserializing(StreamingContext ctx)
        {
            _charLen = -1;
        }

        [OnDeserialized]
        private void OnDeserialized(StreamingContext ctx)
        {
            _strLen = _endIndex + 1;
            _currTextElementLen = _nextTextElementLen;

            if (_charLen == -1)
            {
                _uc = CharUnicodeInfo.InternalGetUnicodeCategory(_str, _index, out _charLen);
            }
        }

        [OnSerializing]
        private void OnSerializing(StreamingContext ctx)
        {
            _endIndex = _strLen - 1;
            _nextTextElementLen = _currTextElementLen;
        }

        public bool MoveNext()
        {
            if (_index >= _strLen)
            {
                // Make the _index to be greater than _strLen so that we can throw exception if GetTextElement() is called.
                _index = _strLen + 1;
                return (false);
            }
            _currTextElementLen = StringInfo.GetCurrentTextElementLen(_str, _index, _strLen, ref _uc, ref _charLen);
            _index += _currTextElementLen;
            return (true);
        }

        //
        // Get the current text element.
        //

        public Object Current
        {
            get
            {
                return (GetTextElement());
            }
        }

        //
        // Get the current text element.
        //

        public String GetTextElement()
        {
            if (_index == _startIndex)
            {
                throw new InvalidOperationException(SR.InvalidOperation_EnumNotStarted);
            }
            if (_index > _strLen)
            {
                throw new InvalidOperationException(SR.InvalidOperation_EnumEnded);
            }

            return (_str.Substring(_index - _currTextElementLen, _currTextElementLen));
        }

        //
        // Get the starting index of the current text element.
        //

        public int ElementIndex
        {
            get
            {
                if (_index == _startIndex)
                {
                    throw new InvalidOperationException(SR.InvalidOperation_EnumNotStarted);
                }
                return (_index - _currTextElementLen);
            }
        }


        public void Reset()
        {
            _index = _startIndex;
            if (_index < _strLen)
            {
                // If we have more than 1 character, get the category of the current char.
                _uc = CharUnicodeInfo.InternalGetUnicodeCategory(_str, _index, out _charLen);
            }
        }
    }
}
